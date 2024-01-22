#!/usr/bin/env python3
"""
Bogcode Penetration Test IDE
Copyright (C) 2013  Infobyte LLC (http://www.threatcodesec.com/)
See the file 'doc/LICENSE' for the license information
"""
# Related third party imports
import click

# Local application imports
import bogcode.server.config
from bogcode.server.commands.initdb import InitDB
from bogcode.server.models import db
from bogcode.server.app import get_app


def reset_db_all():
    # It might be  required to do a cascade delete to correctly the
    # vulnerability table
    for table in ('vulnerability', 'vulnerability_template', 'comment',
                  'bogcode_user'):
        try:
            db.engine.execute(f'DROP TABLE {table} CASCADE')
        except Exception as ex:
            print(ex)
    db.drop_all()

    # db.create_all()
    # Ugly hack to create tables and also setting alembic revision
    conn_string = bogcode.server.config.database.connection_string
    InitDB()._create_tables(conn_string)


def reset_db():
    with get_app().app_context():
        reset_db_all()


@click.command()
@click.option('--confirm/--not-confirm', prompt='Confirm database reset?')
def main(confirm):
    if confirm:
        reset_db()


if __name__ == '__main__':
    main()
