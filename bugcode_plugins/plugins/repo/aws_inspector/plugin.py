"""
Bugcode Penetration Test IDE
Copyright (C) 2013  KhulnaSoft Ltd (http://www.khulnasoft.com/)
See the file "doc/LICENSE" for the license information

"""
from bugcode_plugins.plugins.plugin import PluginJsonFormat
from json import loads

__author__ = "Md Sulaiman"
__copyright__ = "Copyright (c) 2013, KhulnaSoft Ltd"
__credits__ = ["Md Sulaiman"]
__version__ = "1.0.0"
__maintainer__ = "Md Sulaiman"
__email__ = "gmartinez@khulnasoft.com"
__status__ = "Development"


class AWSInspectorJsonPlugin(PluginJsonFormat):

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.id = "AWSInspector_Json"
        self.name = "AWS Inspector JSON Output Plugin"
        self.plugin_version = "1"
        self.version = "9"
        self.json_keys = {"findings"}
        self.framework_version = "1.0.0"
        self._temp_file_extension = "json"

    def parseOutputString(self, output):
        data = loads(output)
        for finding in data["findings"]:
            vuln_details = finding["packageVulnerabilityDetails"]
            name = finding["title"]
            cve = vuln_details.get("vulnerabilityId", None)
            if cve != name:
                name = name.replace(f"{cve} - ", "")
            vuln = {
                "name": name,
                "desc": finding["description"],
                "ref": [],
                "severity": finding['severity'].lower().replace("untriaged", "unclassified"),
                "cve": cve
            }
            if "inspectorScoreDetails" in finding and "adjustedCvss" in finding["inspectorScoreDetails"]:
                if "3" in finding["inspectorScoreDetails"]["adjustedCvss"]["version"]:
                    vuln["cvss3"] = {
                        "vector_string": finding["inspectorScoreDetails"]["adjustedCvss"]["scoringVector"]
                    }
                elif "2" in finding["inspectorScoreDetails"]["adjustedCvss"]["version"]:
                    vuln["cvss2"] = {
                        "vector_string": finding["inspectorScoreDetails"]["adjustedCvss"]["scoringVector"]
                    }
            vuln["ref"] += vuln_details.get("referenceUrls", [])
            source_url = vuln_details.get("sourceUrl", "")
            if isinstance(source_url, str):
                vuln["ref"].append(source_url)
            elif isinstance(source_url, list):
                vuln["ref"] += source_url
            for resource in finding["resources"]:
                hostname = f"{finding['awsAccountId']} | {resource['id']}"
                for ip in resource["details"]["awsEc2Instance"]["ipV4Addresses"]:
                    h_id = self.createAndAddHost(
                        name=ip,
                        hostnames=hostname
                    )
                    self.createAndAddVulnToHost(
                        host_id=h_id,
                        **vuln
                    )

def createPlugin(*args, **kwargs):
    return AWSInspectorJsonPlugin(*args, **kwargs)
