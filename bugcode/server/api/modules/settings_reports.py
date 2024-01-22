"""
Bogcode Penetration Test IDE
Copyright (C) 2021  Infobyte LLC (https://bugcode.com/)
See the file 'doc/LICENSE' for the license information
"""

# Standard library imports
import logging

# Related third party imports
from flask import Blueprint

# Local application imports
from bogcode.settings.reports import ReportsSettingSchema, ReportsSettings
from bogcode.server.api.modules.settings import SettingsAPIView

logger = logging.getLogger(__name__)
reports_settings_api = Blueprint('reports_settings_api', __name__)


class ReportsSettingsAPI(SettingsAPIView):
    route_base = ReportsSettings.settings_id
    schema_class = ReportsSettingSchema


ReportsSettingsAPI.register(reports_settings_api)
