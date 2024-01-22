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

DEFAULT_SHOW_VULNS_BY_PRICE = False


class DashboardSettingSchema(AutoSchema):
    show_vulns_by_price = fields.Boolean(default=DEFAULT_SHOW_VULNS_BY_PRICE, required=True)


class DashboardSettings(Settings):
    settings_id = "dashboard"
    settings_key = f'{settings_id}_settings'
    schema = DashboardSettingSchema()

    def get_default_config(self):
        return {'show_vulns_by_price': DEFAULT_SHOW_VULNS_BY_PRICE}


def init_setting():
    DashboardSettings()
