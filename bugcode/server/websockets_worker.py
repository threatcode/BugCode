#!/usr/bin/env python
from bogcode.server.app import celery, create_app  # noqa
from bogcode.server.extensions import socketio
from bogcode.server.websockets.dispatcher import DispatcherNamespace, remove_sid

app = create_app()

socketio.init_app(app)
with app.app_context():
    remove_sid()
socketio.on_namespace(DispatcherNamespace("/dispatcher"))
