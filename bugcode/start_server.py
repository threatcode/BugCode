# Bugcode Penetration Test IDE
# Copyright (C) 2016  Threatcode LLC (http://www.tthreatcode.github.io/bugcode/)
# See the file 'doc/LICENSE' for the license information
from gevent import monkey
monkey.patch_all()

from psycogreen.gevent import patch_psycopg
patch_psycopg()

import os
import sys
import socket
import argparse
import logging

import psycopg2
from alembic.runtime.migration import MigrationContext

from colorama import init, Fore
import sqlalchemy
from alembic.script import ScriptDirectory
from alembic.config import Config

import bugcode.server.config
from bugcode.server.app import get_app
from bugcode.server.extensions import socketio
from bugcode.server.models import db, Workspace
from bugcode.server.utils import daemonize
from bugcode.server.config import bugcode_server as server_config
from bugcode.server.utils.ping import stop_ping_event
from bugcode.server.utils.reports_processor import stop_reports_event
import sh

logger = logging.getLogger(__name__)

init()


def setup_environment(check_deps=False):
    # Configuration files generation
    bugcode.server.config.copy_default_config_to_local()


def is_server_running(port):
    pid = daemonize.is_server_running(port)
    if pid is not None:
        logger.warning(f"Bugcode Server is already running. PID: {pid}")
        return True
    else:
        return False


def run_server(args):
    daemonize.create_pid_file(args.port)
    app = get_app()
    try:
        if args.with_workers or args.with_workers_gevent:
            if not server_config.celery_enabled:
                print("In order to run bugcode workers you must set `celery_enabled=True` in your server.ini")
                sys.exit()
        if args.with_workers:
            options = {}
            if args.workers_queue:
                options['queue'] = args.workers_queue

            if args.workers_concurrency:
                options['concurrency'] = args.workers_concurrency

            if args.workers_loglevel:
                options['loglevel'] = args.workers_loglevel

            sh.bugcode_worker(**options, _bg=True, _out=sys.stdout)

        elif args.with_workers_gevent:
            options = {}
            if args.workers_concurrency:
                options['concurrency'] = args.workers_concurrency

            sh.bugcode_worker_gevent(**options, _bg=True, _out=sys.stdout)

        socketio.run(app=app,
                     port=server_config.port,
                     host=server_config.bind_address,
                     debug=False)
    except KeyboardInterrupt:
        stop_ping_event.set()
        stop_reports_event.set()
        print("Bugcode server stopped")


def check_postgresql():
    app = get_app()
    with app.app_context():
        try:
            if not db.session.query(Workspace).count():
                logger.warning('No workspaces found')
        except sqlalchemy.exc.ArgumentError:
            logger.error(
                f'\n{Fore.RED}Please check your PostgreSQL connection string in the file ~/.bugcode/config/server.ini'
                f' on your home directory.{Fore.WHITE} \n'
            )
            sys.exit(1)
        except sqlalchemy.exc.OperationalError:
            logger.error(
                    '\n\n{RED}Could not connect to PostgreSQL.\n{WHITE}Please check: \n'
                    '{YELLOW}  * if database is running \n  * configuration settings are correct. \n\n'
                    '{WHITE}For first time installations execute{WHITE}: \n\n'
                    ' {GREEN} bugcode-manage initdb\n\n'.format(GREEN=Fore.GREEN,
                                                                YELLOW=Fore.YELLOW,
                                                                WHITE=Fore.WHITE,
                                                                RED=Fore.RED))
            sys.exit(1)
        except sqlalchemy.exc.ProgrammingError:
            logger.error(
                    f'\n\nn{Fore.WHITE}Missing migrations, please execute: \n\nbugcode-manage migrate')
            sys.exit(1)


def check_alembic_version():
    config = Config()
    config.set_main_option("script_location", "migrations")
    script = ScriptDirectory.from_config(config)

    app = get_app()

    head_revision = script.get_current_head()
    with app.app_context():
        try:
            conn = db.session.connection()
        except ImportError:
            if not bugcode.server.config.database.connection_string:
                print("\n\nNo database configuration found. Did you execute \"bugcode-manage initdb\"? \n\n")
                sys.exit(1)
        except sqlalchemy.exc.OperationalError:
            print("Bad Credentials, please check the .bugcode/config/server.ini")
            sys.exit(1)

        context = MigrationContext.configure(conn)

        current_revision = context.get_current_revision()
        if head_revision != current_revision:
            version_path = bugcode.server.config.BUGCODE_BASE / 'migrations' / 'versions'
            if list(version_path.glob(f'{current_revision}_*.py')):
                print('--' * 20)
                print('Missing migrations, please execute: \n\n')
                print('bugcode-manage migrate')
                sys.exit(1)
            else:
                logger.warning(
                    "You are using an unknown schema version. If you are a "
                    "developer, this probably happened because you used branch "
                    "with a schema migration not merged yet. If you are a "
                    "normal user, consider reporting this bug back to us"
                    )


def check_if_db_up():
    try:
        conn = psycopg2.connect(dbname="postgres")
        conn.close()
    except psycopg2.OperationalError as e:
        if "could not connect to server" in e.args[0]:
            print("\n\nCould not ping the Postgres server, please check if it is running \n\n")
            sys.exit(1)


def main():
    print("Initializing bugcode server")
    os.chdir(bugcode.server.config.BUGCODE_BASE)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='run Bugcode Server in debug mode')
    parser.add_argument('--nodeps', action='store_true', help='Skip dependency check')
    parser.add_argument('--no-setup', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--port', type=int, help='Overides server.ini port configuration')
    parser.add_argument('--bind_address', help='Overides server.ini bind_address configuration')
    parser.add_argument('-v', '--version', action='version', version=f'Bugcode v{bugcode.__version__}')
    parser.add_argument('--with-workers', action='store_true', help='Starts a celery workers')
    parser.add_argument('--with-workers-gevent', action='store_true', help='Run workers in gevent mode')
    parser.add_argument('--workers-queue', help='Celery queue')
    parser.add_argument('--workers-concurrency', help='Celery concurrency')
    parser.add_argument('--workers-loglevel', help='Celery loglevel')
    args = parser.parse_args()
    check_alembic_version()
    # TODO RETURN TO prev CWD
    check_postgresql()
    if args.debug or bugcode.server.config.bugcode_server.debug:
        bugcode.server.utils.logger.set_logging_level(bugcode.server.config.DEBUG)
    args.port = bugcode.server.config.bugcode_server.port = args.port or \
            bugcode.server.config.bugcode_server.port or 5985
    if args.bind_address:
        bugcode.server.config.bugcode_server.bind_address = args.bind_address

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((args.bind_address or bugcode.server.config.bugcode_server.bind_address,
                              int(args.port or bugcode.server.config.bugcode_server.port)))
    if is_server_running(args.port) and result == 0:
        sys.exit(1)
    if result == 0:
        logger.error("Bugcode Server port in use. Check your processes and run the server again...")
        sys.exit(1)
    if not args.no_setup:
        setup_environment(not args.nodeps)
    run_server(args)


if __name__ == '__main__':  # Don't delete. this is used for dev
    main()
