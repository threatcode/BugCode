"""
Bogcode Penetration Test IDE
Copyright (C) 2016  Infobyte LLC (https://bugcode.com/)
See the file 'doc/LICENSE' for the license information
"""

# Related third party imports
import flask
from flask import Blueprint
from marshmallow import Schema

# Local application imports
from bogcode import __version__ as f_version
from bogcode.server.api.base import GenericView
from bogcode.server.config import bogcode_server
from bogcode.settings.dashboard import DashboardSettings

info_api = Blueprint('info_api', __name__)


class EmptySchema(Schema):
    pass


class InfoView(GenericView):
    route_base = 'info'
    schema_class = EmptySchema

    def get(self):
        """
        ---
        get:
          tags: ["Informational"]
          description: Gives basic info about the bogcode service
          responses:
            200:
              description: Ok
        """

        response = flask.jsonify({'Bogcode Server': 'Running', 'Version': f_version})
        response.status_code = 200

        return response

    get.is_public = True


class ConfigView(GenericView):
    route_base = 'config'
    route_prefix = ''
    schema_class = EmptySchema

    def get(self):
        """
        ---
        get:
          tags: ["Informational"]
          description: Gives basic info about the bogcode configuration
          responses:
            200:
              description: Ok
        """
        doc = {
            'ver': f_version,
            'websocket_port': bogcode_server.websocket_port,
            'show_vulns_by_price': DashboardSettings.settings.show_vulns_by_price,
            'smtp_enabled': False
        }

        return flask.jsonify(doc)

    get.is_public = True


InfoView.register(info_api)
ConfigView.register(info_api)
