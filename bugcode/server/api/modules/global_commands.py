# Bugcode Penetration Test IDE
# Copyright (C) 2016  Threatcode LLC (http://www.threatcodesec.com/)
# See the file 'doc/LICENSE' for the license information
import logging

from flask import Blueprint

from bugcode.server.api.base import (
    ReadOnlyView,
    PaginatedMixin
)
from bugcode.server.models import Command
from bugcode.server.api.modules.commandsrun import CommandSchema

globalcommands_api = Blueprint('globalcommands_api', __name__)
logger = logging.getLogger(__name__)


class GlobalCommandView(ReadOnlyView, PaginatedMixin):
    route_base = 'global_commands'
    model_class = Command
    schema_class = CommandSchema
    order_field = Command.start_date.desc()

    def _envelope_list(self, objects, pagination_metadata=None):
        commands = []
        for command in objects:
            commands.append({
                'id': command['_id'],
                'key': command['_id'],
                'value': command
            })
        return {
            'commands': commands,
        }


GlobalCommandView.register(globalcommands_api)
