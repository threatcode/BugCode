#!/usr/bin/env python
from bugcode.server.app import celery, create_app  # noqa
from bugcode.server.extensions import socketio
from bugcode.server.websockets.dispatcher import DispatcherNamespace, remove_sid

app = create_app()

socketio.init_app(app)
with app.app_context():
    remove_sid()
socketio.on_namespace(DispatcherNamespace("/dispatcher"))
