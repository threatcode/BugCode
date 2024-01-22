"""
Bugcode Penetration Test IDE
Copyright (C) 2013  KhulnaSoft Ltd (http://www.khulnasoft.com/)
See the file 'doc/LICENSE' for the license information

"""

import xml.etree.ElementTree as ET

from dateutil.parser import parse
from bugcode_plugins.plugins.plugin import PluginXMLFormat

__author__ = "Blas"
__copyright__ = "Copyright (c) 2019, KhulnaSoft Ltd"
__credits__ = ["Blas", "Nicolas Rebagliati"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Blas"
__email__ = "bmoyano@khulnasoft.com"
__status__ = "Development"

from bugcode_plugins.plugins.repo.nessus.DTO import ReportHost, Report, ReportItem
from bugcode_plugins.plugins.plugins_utils import get_severity_from_cvss

class NessusParser:
    """
    The objective of this class is to parse an xml file generated by the nessus tool.

    TODO: Handle errors.
    TODO: Test nessus output version. Handle what happens if the parser doesn't support it.
    TODO: Test cases.

    @param nessus_filepath A proper simple report generated by nessus
    """

    def __init__(self, output):
        self.tree = ET.fromstring(output)
        self.report = []
        if self.tree:
            self.report = self.__get_report()

    def __get_report(self) -> Report:
        report = self.tree.find('Report')
        return Report(report) if report else None


class NessusPlugin(PluginXMLFormat):
    """
    Example plugin to parse nessus output.
    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.extension = ".nessus"
        self.identifier_tag = "NessusClientData_v2"
        self.id = "Nessus"
        self.name = "Nessus XML Output Plugin"
        self.plugin_version = "0.0.1"
        self.version = "5.2.4"
        self.framework_version = "1.0.1"
        self.options = None

    @staticmethod
    def parse_compliance_data(data: dict):
        compliance_data = {}
        for key, value in data.items():
            if 'compliance-' in key:
                compliance_name = key.split("}")[-1]
                compliance_data[compliance_name] = value
        return compliance_data

    def map_properties(self, host: ReportHost):
        if self.hostname_resolution:
            name = host.host_properties.host_ip if host.host_properties.host_ip else host.name
        else:
            name = host.name
        hostnames = [host.host_properties.host_fqdn]
        if host.host_properties.host_rdns and host.host_properties.host_rdns not in hostnames:
            hostnames.append(host.host_properties.host_rdns)
        return {
            "name": name,
            "hostnames": hostnames,
            "mac": host.host_properties.mac_address,
            "os": host.host_properties.operating_system
        }

    @staticmethod
    def map_item(host_id, run_date, plugin_name, item: ReportItem) -> dict:
        data = item.plugin_output
        data += f'{item.exploit_available}'
        return {
            "host_id": host_id,
            "name": plugin_name,
            "severity": item.risk_factor,
            "data": data,
            "external_id": item.plugin_id_attr,
            "run_date": run_date,
            "desc": item.description,
            "resolution": item.solution,
            "ref": [],
        }

    def map_policy_general(self, kwargs, item: ReportItem):
        kwargs.update({"policyviolations": []})
        if item.plugin_family_attr == 'Policy Compliance':
            data = item.get_data()
            bis_benchmark_data = kwargs["desc"].split('\n')
            compliance_data = self.parse_compliance_data(data)
            compliance_info = compliance_data.get('compliance-info', '')
            if compliance_info and not kwargs["desc"]:
                kwargs["desc"] = compliance_info
            compliance_reference = compliance_data.get(
                'compliance-reference', '').replace('|', ':').split(',')
            compliance_result = compliance_data.get('compliance-result', '')
            for reference in compliance_reference:
                kwargs["ref"].append(reference)
            compliance_check_name = compliance_data.get('compliance-check-name', '')
            compliance_solution = compliance_data.get('compliance-solution', '')
            if compliance_solution and not kwargs["resolution"]:
                kwargs["resolution"] = compliance_solution
            policy_item = f'{compliance_check_name} - {compliance_result}'
            for policy_check_data in bis_benchmark_data:
                if 'ref.' in policy_check_data:
                    kwargs["ref"].append(policy_check_data)
            if 'compliance-see-also' in compliance_data:
                kwargs["ref"].append(compliance_data.get('compliance-see-also'))
            # We used this info from tenable: https://community.tenable.com/s/article/Compliance-checks-in-SecurityCenter
            kwargs["policyviolations"].append(policy_item)
            kwargs["name"] = f'{kwargs["name"]}: {policy_item}'

        return kwargs

    def parseOutputString(self, output):
        """
        This method will discard the output the shell sends, it will read it from
        the xml where it expects it to be present.

        NOTE: if 'debug' is true then it is being run from a test case and the
        output being sent is valid.
        """

        try:
            parser = NessusParser(output)
        except Exception as e:
            self.logger.error(str(e))
            return None
        report_hosts = parser.report.report_hosts
        if report_hosts:
            for host in report_hosts:
                run_date = host.host_properties.host_end
                if run_date:
                    run_date = parse(run_date)
                website = host.host_properties.host_fqdn
                host_id = self.createAndAddHost(**self.map_properties(host))

                for item in host.report_items:
                    vulnerability_name = item.plugin_name
                    if not vulnerability_name:
                        continue
                    item_name = item.svc_name_attr

                    main_data = self.map_item(
                        host_id, run_date, vulnerability_name, item)

                    main_data = self.map_add_ref(main_data, item)
                    if item_name == 'general':
                        main_data = self.map_policy_general(main_data, item)
                        self.createAndAddVulnToHost(**main_data)
                    else:
                        main_data["service_id"] = self.createAndAddServiceToHost(
                            host_id, name=item_name, protocol=item.protocol_attr,
                            ports=item.port_attr)
                        if item_name == 'www' or item_name == 'http':
                            main_data.update({"website": website})
                            self.createAndAddVulnWebToService(**main_data)
                        else:
                            self.createAndAddVulnToService(**main_data)

    @staticmethod
    def map_add_ref(main_data, item: ReportItem):
        main_data["cvss2"] = {}
        main_data["cvss3"] = {}
        if item.see_also:
            main_data["ref"].append(item.see_also)
        if item.cpe:
            main_data["ref"].append(item.cpe)
        if item.cve:
            main_data["cve"] = item.cve
        if item.cwe:
            main_data["cwe"] = item.cwe
        if item.cvss3_vector:
            main_data["cvss3"]["vector_string"] = item.cvss3_vector
        #if item has cvss3.base_score use it for severity
        if item.cvss3_base_score:
            main_data["severity"] = get_severity_from_cvss(item.cvss3_base_score)
        if item.cvss_vector:
            main_data["cvss2"]["vector_string"] = item.cvss_vector
        return main_data


def createPlugin(*args, **kwargs):
    return NessusPlugin(*args, **kwargs)