"""
Bugcode Penetration Test IDE
Copyright (C) 2019  KhulnaSoft Ltd (http://www.khulnasoft.com/)
See the file 'doc/LICENSE' for the license information

"""
import json
import re
from urllib.parse import urlparse

from bugcode_plugins.plugins.plugin import PluginJsonFormat

__author__ = "Nicolas Rebagliati"
__copyright__ = "Copyright (c) 2019, KhulnaSoft Ltd"
__credits__ = ["Nicolas Rebagliati"]
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Nicolas Rebagliati"
__email__ = "nrebagliati@khulnasoft.com"
__status__ = "Development"


class WPScanJsonParser:

    def __init__(self, json_output, resolve_hostname):
        self.json_data = json.loads(json_output)
        self.resolve_hostname = resolve_hostname

    def parse_url(self, url):
        # Strips protocol and gets hostname from URL.

        url_parse = urlparse(url)
        protocol = url_parse.scheme
        hostname = url_parse.netloc
        port = url_parse.port

        if protocol == 'https':
            port = 443
        elif protocol == 'http':
            if not port:
                port = 80
        address = self.resolve_hostname(hostname)
        return {'protocol': protocol, 'hostname': hostname, 'port': port, 'address': address}


class WPScanPlugin(PluginJsonFormat):
    """ Handle the WPScan tool. Detects the output of the tool
    and adds the information to Bugcode.
    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.id = "wpscan"
        self.name = "WPscan"
        self.plugin_version = "0.2"
        self.version = "3.4.5"
        self.json_keys = [{"target_url", "effective_url", "interesting_findings"},
                          {"target_url", "effective_url", "plugins"}]
        self._command_regex = re.compile(r'^(sudo wpscan|wpscan)\s+.*?')
        self._use_temp_file = True
        self._temp_file_extension = "json"

    def parseOutputString(self, output):
        parser = WPScanJsonParser(output, self.resolve_hostname)
        url_data = parser.parse_url(parser.json_data['target_url'])
        host_id = self.createAndAddHost(url_data['address'], hostnames=[url_data['hostname']])
        service_id = self.createAndAddServiceToHost(
            host_id,
            "WordPress",
            url_data['protocol'],
            ports=[url_data['port']],
            status='open',
            version='',
            description='')
        for user, data in parser.json_data.get('users', {}).items():
            self.createAndAddCredToService(host_id, service_id, user, "")
        main_theme = parser.json_data.get("main_theme", {})
        if main_theme:
            for vuln in main_theme.get("vulnerabilities", []):
                wpvulndb = ",".join(vuln['references'].get('wpvulndb', []))
                self.createAndAddVulnWebToService(host_id, service_id, vuln['title'], ref=vuln['references'].get('url', []),
                                                  severity='unclassified', external_id=wpvulndb)
        for plugin, plugin_data in parser.json_data.get("plugins", {}).items():
            for vuln in plugin_data['vulnerabilities']:
                wpvulndb = ",".join(vuln['references'].get('wpvulndb', []))
                cve = ["CVE-"+ cve for cve in vuln['references'].get('cve')] if vuln['references'].get('cve') else []
                self.createAndAddVulnWebToService(host_id, service_id, f"{plugin}: {vuln['title']}",
                                                  ref=vuln['references'].get('url', []),
                                                  severity='unclassified', external_id=wpvulndb, cve=cve)
        for vuln in parser.json_data.get("interesting_findings", []):
            if vuln['to_s'].startswith('http'):
                vuln_name = f"{vuln['type']}: {vuln['to_s']}"
            else:
                vuln_name = vuln['to_s']
            self.createAndAddVulnWebToService(host_id, service_id, vuln_name, ref=vuln['references'].get('url', []),
                                              severity='unclassified')

    def processCommandString(self, username, current_path, command_string):
        """
        Adds the path to a temporary file parameter to get .json output to the command string that the
        user has set.
        """
        super().processCommandString(username, current_path, command_string)
        command_string += f" --output={self._output_file_path} --format json"
        return command_string


def createPlugin(*args, **kwargs):
    return WPScanPlugin(*args, **kwargs)
