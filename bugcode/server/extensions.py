"""
Bugcode Penetration Test IDE
Copyright (C) 2021  Threatcode LLC (https://threatcode.github.io/bugcode/)
See the file 'doc/LICENSE' for the license information
"""
# Related third party imports
from flask_socketio import SocketIO
from flask_celery import Celery

socketio = SocketIO(cors_allowed_origins='*', engineio_logger=True)
celery = Celery()
