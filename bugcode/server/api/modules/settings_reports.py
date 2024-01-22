"""
Bugcode Penetration Test IDE
Copyright (C) 2021  Threatcode LLC (https://threatcode.github.io/bugcode/)
See the file 'doc/LICENSE' for the license information
"""

# Standard library imports
import logging

# Related third party imports
from flask import Blueprint

# Local application imports
from bugcode.settings.reports import ReportsSettingSchema, ReportsSettings
from bugcode.server.api.modules.settings import SettingsAPIView

logger = logging.getLogger(__name__)
reports_settings_api = Blueprint('reports_settings_api', __name__)


class ReportsSettingsAPI(SettingsAPIView):
    route_base = ReportsSettings.settings_id
    schema_class = ReportsSettingSchema


ReportsSettingsAPI.register(reports_settings_api)
