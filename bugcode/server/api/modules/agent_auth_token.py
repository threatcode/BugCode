"""
Bugcode Penetration Test IDE
Copyright (C) 2016  Threatcode LLC (https://threatcode.github.io/bugcode/)
See the file 'doc/LICENSE' for the license information
"""

# Standard library imports
import datetime

# Related third party imports
import pyotp
from flask import Blueprint
from marshmallow import fields, Schema

# Local application imports
from bugcode.server.api.base import GenericView
from bugcode.server.config import bugcode_server

agent_auth_token_api = Blueprint('agent_auth_token_api', __name__)


class AgentAuthTokenSchema(Schema):
    token = fields.String(required=True)
    expires_in = fields.Float(required=True)
    total_duration = fields.Float(required=True)


class AgentAuthTokenView(GenericView):
    route_base = 'agent_token'
    schema_class = AgentAuthTokenSchema

    def index(self):
        """
          ---
          get:
            summary: "Get the current TOTP token to register new agents."
            tags: ["Agent"]
            responses:
              200:
                description: Ok
                content:
                  application/json:
                    schema: AgentAuthTokenSchema
          tags: ["Agent"]
          responses:
            200:
              description: Ok
        """
        totp = pyotp.TOTP(bugcode_server.agent_registration_secret, interval=int(
            bugcode_server.agent_token_expiration))
        return AgentAuthTokenSchema().dump(
            {'token': totp.now(),
             'expires_in': totp.interval - datetime.datetime.utcnow().timestamp() % totp.interval,
             'total_duration': totp.interval})


AgentAuthTokenView.register(agent_auth_token_api)
