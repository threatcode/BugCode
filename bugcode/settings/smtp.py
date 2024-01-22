"""
Bugcode Penetration Test IDE
Copyright (C) 2021  Threatcode LLC (https://threatcode.github.io/bugcode/)
See the file 'doc/LICENSE' for the license information
"""
# Related third party imports
from marshmallow import fields

# Local application imports
from bugcode.server.api.base import AutoSchema
from bugcode.settings.base import Settings
from bugcode.settings.exceptions import InvalidConfigurationError

DEFAULT_ENABLED = False
DEFAULT_USERNAME = ""
DEFAULT_PASSWORD = ""  # nosec
DEFAULT_HOST = ""
DEFAULT_PORT = 25
DEFAULT_SENDER = ""
DEFAULT_SSL = False


class SMTPSettingSchema(AutoSchema):
    enabled = fields.Boolean(default=DEFAULT_ENABLED, required=True)
    username = fields.String(default=DEFAULT_USERNAME, required=True)
    password = fields.String(default=DEFAULT_PASSWORD, required=True)
    host = fields.String(default=DEFAULT_HOST, required=True)
    port = fields.Integer(default=DEFAULT_PORT, required=True)
    sender = fields.Email(default="user@example.com", required=True)
    ssl = fields.Boolean(default=DEFAULT_SSL, required=True)


class SMTPSettings(Settings):
    settings_id = "smtp"
    settings_key = f'{settings_id}_settings'
    schema = SMTPSettingSchema()

    def custom_validation(self, validated_config):
        if validated_config['enabled']:
            for field in ('username', 'password', 'host'):
                if not validated_config[field]:
                    raise InvalidConfigurationError(f"{field} is required if smtp is enabled")

    def get_default_config(self):
        return {'enabled': DEFAULT_ENABLED, 'username': DEFAULT_USERNAME, 'password': DEFAULT_PASSWORD,
                'host': DEFAULT_HOST, 'port': DEFAULT_PORT, 'sender': DEFAULT_SENDER, 'ssl': DEFAULT_SSL}


def init_setting():
    SMTPSettings()
