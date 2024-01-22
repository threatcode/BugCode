"""
Bugcode Penetration Test IDE
Copyright (C) 2013  KhulnaSoft Ltd (http://www.khulnasoft.com/)
See the file 'doc/LICENSE' for the license information

"""
import re

from bugcode_plugins.plugins.plugin import PluginBase

__author__ = "Francisco Amato"
__copyright__ = "Copyright (c) 2013, KhulnaSoft Ltd"
__credits__ = ["Francisco Amato"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Francisco Amato"
__email__ = "famato@khulnasoft.com"
__status__ = "Development"


class DnswalkParser:
    """
    The objective of this class is to parse an xml file generated
    by the dnswalk tool.

    TODO: Handle errors.
    TODO: Test dnswalk output version. Handle what happens if the parser
    doesn't support it.
    TODO: Test cases.

    @param dnswalk_filepath A proper simple report generated by dnswalk
    """

    def __init__(self, output, resolve_hostName):

        lists = output.split("\n")
        self.items = []
        self.resolve_hostName = resolve_hostName

        for line in lists:
            mregex = re.search(r"WARN: ([\w\.]+) ([\w]+) ([\w\.]+):", line)
            if mregex is not None:
                item = {
                    'host': mregex.group(1),
                    'ip': mregex.group(3),
                    'type': mregex.group(2)}

                self.items.append(item)

            mregex = re.search(
                r"Getting zone transfer of ([\w\.]+) from ([\w\.]+)\.\.\.done\.",
                line)

            if mregex is not None:
                ip = self.resolve_hostname(mregex.group(2))
                item = {
                    'host': mregex.group(1),
                    'ip': ip,
                    'type': 'info'}
                self.items.append(item)


class DnswalkPlugin(PluginBase):
    """
    Example plugin to parse dnswalk output.
    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.id = "Dnswalk"
        self.name = "Dnswalk XML Output Plugin"
        self.plugin_version = "0.0.1"
        self.version = "2.0.2"
        self.options = None
        self._current_output = None
        self._command_regex = re.compile(
            r'^(sudo dnswalk|dnswalk|\.\/dnswalk)\s+.*?')

    def canParseCommandString(self, current_input):
        if self._command_regex.match(current_input.strip()):
            self.command = self.get_command(current_input)
            return True
        else:
            return False

    def parseOutputString(self, output):
        """
        output is the shell output of command Dnswalk.
        """
        parser = DnswalkParser(output, self.resolve_hostname)

        for item in parser.items:
            if item['type'] == "A":
                h_id = self.createAndAddHost(item['ip'], hostnames=[item['host']])
            elif item['type'] == "info":
                h_id = self.createAndAddHost(item['ip'], hostnames=[item['host']])
                s_id = self.createAndAddServiceToHost(
                    h_id,
                    "domain",
                    "tcp",
                    ports=['53'])
                self.createAndAddVulnToService(
                    h_id,
                    s_id,
                    "Zone transfer",
                    desc="A Dns server allows unrestricted zone transfers",
                    ref=["CVE-1999-0532"])

        return True


def createPlugin(*args, **kwargs):
    return DnswalkPlugin(*args, **kwargs)
