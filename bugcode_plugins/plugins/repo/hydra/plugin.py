"""
Bugcode Penetration Test IDE
Copyright (C) 2013  KhulnaSoft Ltd (http://www.khulnasoft.com/)
See the file 'doc/LICENSE' for the license information
"""
from bugcode_plugins.plugins.plugin import PluginBase
import re
from collections import defaultdict

__author__ = "NxPKG"
__copyright__ = "Copyright (c) 2013, KhulnaSoft Ltd"
__credits__ = ["NxPKG"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "NxPKG"
__email__ = "famato@khulnasoft.com"
__status__ = "Development"


class HydraParser:
    """
    The objective of this class is to parse an xml file generated by the hydra tool.

    @param hydra_filepath A proper simple report generated by hydra
    """

    def __init__(self, xml_output):
        lines = xml_output.splitlines()
        self.items = []
        for line in lines:

            reg = re.search(
                r"\[([^$]+)\]\[([^$]+)\] host: ([^$]+)   login: ([^$]+)   password: ([^$]+)",
                line)

            if reg:
                item = {
                    'port': reg.group(1),
                    'plugin': reg.group(2),
                    'ip': reg.group(3),
                    'login': reg.group(4),
                    'password': reg.group(5)}

                self.items.append(item)


class HydraPlugin(PluginBase):
    """
    Example plugin to parse hydra output.
    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.id = "Hydra"
        self.name = "Hydra XML Output Plugin"
        self.plugin_version = "0.0.1"
        self.version = "7.5"
        self.options = None
        self._command_regex = re.compile(r'^(sudo hydra|sudo \.\/hydra|hydra|\.\/hydra)\s+.*?')
        self.host = None
        self._use_temp_file = True
        self._temp_file_extension = "txt"
        self.xml_arg_re = re.compile(r"^.*(-o\s*[^\s]+).*$")

    def parseOutputString(self, output):
        """
        This method will discard the output the shell sends, it will read it from
        the xml where it expects it to be present.

        NOTE: if 'debug' is true then it is being run from a test case and the
        output being sent is valid.
        """

        parser = HydraParser(output)
        hosts = defaultdict(list)
        service = ''
        port = ''

        for item in parser.items:

            service = item['plugin']
            port = item['port']
            hosts[item['ip']].append([item['login'], item['password']])

        for k, v in hosts.items():
            ip = self.resolve_hostname(k)
            if ip != k:
                hostnames = [k]
            else:
                hostnames = None
            h_id = self.createAndAddHost(ip, hostnames=hostnames)
            s_id = self.createAndAddServiceToHost(
                h_id,
                service,
                ports=[port],
                protocol="tcp",
                status="open")

            for cred in v:
                self.createAndAddCredToService(
                    h_id,
                    s_id,
                    cred[0],
                    cred[1])

                self.createAndAddVulnToService(
                    h_id,
                    s_id,
                    "Weak Credentials",
                    f"[hydra found the following credentials]\nuser:{cred[0]}\npass:{cred[1]}",
                    severity="high")

        del parser

    def processCommandString(self, username, current_path, command_string):
        super().processCommandString(username, current_path, command_string)
        arg_match = self.xml_arg_re.match(command_string)
        if arg_match is None:
            return re.sub(r"(^.*?hydra?)", r"\1 -o %s" % self._output_file_path, command_string)
        else:
            return re.sub(arg_match.group(1), r"-o %s" % self._output_file_path, command_string)

    def _isIPV4(self, ip):
        if len(ip.split(".")) == 4:
            return True
        else:
            return False




def createPlugin(*args, **kwargs):
    return HydraPlugin(*args, **kwargs)
