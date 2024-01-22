import re
from collections import defaultdict
from copy import copy
"""
Bugcode Penetration Test IDE
Copyright (C) 2013  KhulnaSoft Ltd (http://www.khulnasoft.com/)
See the file 'doc/LICENSE' for the license information

"""

from bugcode_plugins.plugins.plugin import PluginXMLFormat
from bugcode_plugins.plugins.plugins_utils import filter_services

import xml.etree.ElementTree as ET

__author__ = "Francisco Amato"
__copyright__ = "Copyright (c) 2013, KhulnaSoft Ltd"
__credits__ = ["Francisco Amato"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Francisco Amato"
__email__ = "famato@khulnasoft.com"
__status__ = "Development"


class OpenvasXmlParser:
    """
    The objective of this class is to parse an xml file generated by the openvas tool.

    TODO: Handle errors.
    TODO: Test openvas output version. Handle what happens if the parser doesn't support it.
    TODO: Test cases.

    @param openvas_xml_filepath A proper xml generated by openvas
    """

    def __init__(self, xml_output, logger):
        self.target = None
        self.port = "80"
        self.host = None
        self.logger = logger
        tree = self.parse_xml(xml_output)
        if tree:
            self.hosts = self.get_hosts(tree)
            self.items = list(self.get_items(tree, self.hosts))
        else:
            self.items = []

    def parse_xml(self, xml_output):
        """
        Open and parse an xml file.

        TODO: Write custom parser to just read the nodes that we need instead of
        reading the whole file.

        @return xml_tree An xml tree instance. None if error.
        """
        try:
            tree = ET.fromstring(xml_output)
        except SyntaxError as err:
            self.logger.error("SyntaxError: %s. %s", err, xml_output)
            return None
        return tree

    def get_items(self, tree, hosts):
        """
        @return items A list of Host instances
        """
        try:
            report = tree.find('report')
            if report:
                results = report.findall('results')
                if results:
                    nodes = report.findall('results')[0]
                else:
                    nodes = tree.findall('result')
            else:
                nodes = tree.findall('result')

            for node in nodes:
                try:
                    yield Item(node, hosts)
                except Exception as e:
                    self.logger.error(f"Error generating Iteem from {node.attrib} [{e}]")

        except Exception as e:
            self.logger.error(f"Tag not found: {e}")

    def get_hosts(self, tree):
        # Hosts are located in: /report/report/host
        # hosts_dict will contain has keys its details and its hostnames
        hosts = tree.findall('report/host')
        hosts_dict = {}
        for host in hosts:
            ip = self.do_clean(host.find('ip').text)
            details = self.get_data_from_detail(host.findall('detail'))
            hosts_dict[ip] = details
        return hosts_dict

    def get_data_from_detail(self, details):
        data = {}
        details_data = defaultdict(list)
        hostnames = []
        for item in details:
            name = self.do_clean(item.find('name').text)
            value = self.do_clean(item.find('value').text)
            if "EXIT" in name:
                continue
            if name == 'hostname':
                hostnames.append(value)
            else:
                details_data[name].append(value)
        data['details'] = details_data
        data['hostnames'] = hostnames
        return data

    def do_clean(self, value):
        myreturn = ""
        if value is not None:
            myreturn = re.sub(r"\s+", " ", value)
        return myreturn.strip()


def get_attrib_from_subnode(xml_node, subnode_xpath_expr, attrib_name):
    """
    Finds a subnode in the item node and the retrieves a value from it

    @return An attribute value
    """

    node = xml_node.find(subnode_xpath_expr)

    if node is not None:
        return node.get(attrib_name)

    return None


class Item:
    """
    An abstract representation of a Item
    @param item_node A item_node taken from an openvas xml tree
    """

    def __init__(self, item_node, hosts):
        self.node = item_node
        self.host = self.get_text_from_subnode('host')
        self.threat = self.get_text_from_subnode('threat')
        self.subnet = self.get_text_from_subnode('subnet')
        if self.subnet == '':
            self.subnet = self.host
        self.port = None
        self.severity = self.severity_mapper()
        self.severity_nr = self.get_text_from_subnode("severity")
        self.service = "Unknown"
        self.protocol = ""
        details = self.node.findall("detection/result/details/detail")
        self.cpe = details[0].findtext("value") if details else None
        port_string = self.get_text_from_subnode('port')
        info = port_string.split("/")
        if len(info) < 2:
            info = details[1].findtext("value").split("/") if details else ["", ""]
        self.protocol = "".join(filter(lambda x: x.isalpha() or x in ("-", "_"), info[1]))
        self.port = "".join(filter(lambda x: x.isdigit(), info[0])) or None
        if not self.port:
            self.service = info[0]
        else:
            if hosts:
                host_details = hosts[self.host].get('details')
                self.service = self.get_service(port_string, self.port, host_details)
            else:
                self.service = "Not Service"
        self.nvt = self.node.findall('nvt')[0]
        self.node = self.nvt
        self.id = self.node.get('oid')
        self.cvss_base = self.get_text_from_subnode("cvss_base")
        self.name = self.get_text_from_subnode('name')
        self.cve = self.get_text_from_subnode('cve') if self.get_text_from_subnode('cve') != "NOCVE" else ""
        self.bid = self.get_text_from_subnode('bid') if self.get_text_from_subnode('bid') != "NOBID" else ""
        self.xref = self.get_text_from_subnode('xref') if self.get_text_from_subnode('xref') != "NOXREF" else ""
        self.cwe = []
        if "URL:https://cwe.mitre.org/data/definitions/" in self.xref:
            self.cwe.append("CWE-"+self.xref.split("URL:https://cwe.mitre.org/data/definitions/")[1]
                            .replace("html", ""))
        self.description = ''
        self.resolution = ''
        self.cvss_vector = ''
        self.tags = self.get_text_from_subnode('tags')
        self.data = self.get_text_from_subnode('description')
        self.data += f'\n\nid {item_node.attrib.get("id")}'
        if self.tags:
            tags_data = self.get_data_from_tags(self.tags)
            self.description = tags_data['description']
            self.resolution = tags_data['solution']
            self.cvss_vector = tags_data['cvss_base_vector']
            if tags_data['impact']:
                self.data += f'\n\nImpact: {tags_data["impact"]}'

    def get_text_from_subnode(self, subnode_xpath_expr):
        """
        Finds a subnode in the host node and the retrieves a value from it.

        @return An attribute value
        """
        sub_node = self.node.find(subnode_xpath_expr)
        if sub_node is not None and sub_node.text is not None:
            return sub_node.text.strip()
        return ''

    def severity_mapper(self):
        severity = self.get_text_from_subnode('threat')
        if severity == 'Alarm':
            severity = 'Critical'
        return severity

    def get_service(self, port_string, port, details_from_host):
        # details_from_host:
        # name: name of detail
        # value: list with the values associated with the name
        details_from_host_copy = copy(details_from_host)
        services = details_from_host_copy.pop("Services", None)
        if services:
            service_detail = self.get_service_from_details("Services", services, port)
            if service_detail:
                return service_detail
        for name, value in details_from_host_copy.items():
            service_detail = self.get_service_from_details(name, value, port)
            if service_detail:
                return service_detail
        # if the service is not in details_from_host, we will search it in
        # the file port_mapper.txt
        services_mapper = filter_services()
        for service in services_mapper:
            if service[0] == port_string:
                return service[1]
        return "Unknown"

    def do_clean(self, value):
        myreturn = ""
        if value is not None:
            myreturn = re.sub(r"\s+", " ", value)

        return myreturn.strip()

    def get_service_from_details(self, name, value_list, port):
        # detail:
        # name: name of detail
        # value_list: list with the values associated with the name
        res = None
        priority = 0
        if name == 'Services':
            for value in value_list:
                value_splited = value.split(',')
                if value_splited[0] == port:
                    res = value_splited[2]
                    break
        else:
            for value in value_list:
                if '/' in value:
                    auxiliar_value = value.split('/')[0]
                    if auxiliar_value == port:
                        res = name
                        priority = 2

                elif value.isdigit() and priority == 0:
                    if value == port:
                        res = name
                        priority = 1

                elif '::' in value and priority == 0:
                    aux_value = value.split('::')[0]
                    if aux_value == port:
                        res = name
        return res

    def get_data_from_tags(self, tags_text):
        clean_text = self.do_clean(tags_text)
        tags = clean_text.split('|')
        summary = ''
        insight = ''
        data = {
            'solution': '',
            'cvss_base_vector': '',
            'description': '',
            'impact': ''
        }
        for tag in tags:
            splited_tag = tag.split('=', 1)
            if splited_tag[0] in data.keys():
                data[splited_tag[0]] = splited_tag[1]
            elif splited_tag[0] == 'summary':
                summary = splited_tag[1]
            elif splited_tag[0] == 'insight':
                insight = splited_tag[1]

        data['description'] = ' '.join([summary, insight]).strip()

        return data


class OpenvasPlugin(PluginXMLFormat):
    """
    Example plugin to parse openvas output.
    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.identifier_tag = ["report", "get_results_response"]
        self.id = "Openvas"
        self.name = "Openvas XML Output Plugin"
        self.plugin_version = "0.3"
        self.version = "9.0.3"
        self.framework_version = "1.0.0"
        self.options = None

    def report_belongs_to(self, **kwargs):
        if super().report_belongs_to(**kwargs):
            report_path = kwargs.get("report_path", "")
            with open(report_path) as f:
                output = f.read()
            return re.search("OpenVAS", output) is not None \
                   or re.search('<omp>', output) is not None \
                   or re.search('<owner>', output) is not None
        return False

    def parseOutputString(self, output):
        """
        This method will discard the output the shell sends, it will read it
        from the xml where it expects it to be present.
        """
        parser = OpenvasXmlParser(output, self.logger)
        ids = {}
        # The following threats values will not be taken as vulns
        self.ignored_severities = ['Log', 'Debug']
        for ip, values in parser.hosts.items():
            # values contains: ip details and ip hostnames
            os_report = values['details'].get('best_os_txt')
            h_id = self.createAndAddHost(
                ip,
                os_report[0] if os_report else '',
                hostnames=values['hostnames']
            )
            ids[ip] = h_id
        for item in parser.items:

            if item.name is not None:
                ref = []
                cve = []
                cvss2 = {}
                if item.cve:
                    cves = item.cve.split(',')
                    for i in cves:
                        cve.append(i.strip())
                if item.bid:
                    bids = item.bid.split(',')
                    for bid in bids:
                        ref.append(f"BID-{bid.strip()}")
                if item.xref:
                    ref.append(item.xref)
                if item.tags and item.cvss_vector:
                    cvss2["vector_string"] = item.cvss_vector
                if item.cpe:
                    ref.append(f"{item.cpe}")
                if item.severity_nr:
                    if float(item.severity_nr) >= 9.0:
                        item.threat = "Critical"
                        item.severity = "Critical"
                    ref.append(f"SEVERITY NUMBER: {item.severity_nr}")
                if item.threat:
                    ref.append(f"THREAT: {item.threat}")

                if item.subnet in ids:
                    h_id = ids[item.host]
                else:
                    h_id = self.createAndAddHost(
                        item.subnet,
                        hostnames=[item.host])
                    ids[item.subnet] = h_id

                if not item.port:
                    if item.severity not in self.ignored_severities:
                        v_id = self.createAndAddVulnToHost(
                            h_id,
                            item.name,
                            desc=item.description,
                            severity=item.severity,
                            resolution=item.resolution,
                            ref=ref,
                            external_id=f"OPENVAS-{item.id}",
                            data=item.data,
                            cve=cve,
                            cwe=item.cwe,
                            cvss2=cvss2
                        )
                else:
                    if item.service:
                        web = re.search(
                            r'^(www|http)',
                            item.service)
                    else:
                        web = item.port in ('80', '443', '8080')

                    if item.subnet + "_" + item.port in ids:
                        s_id = ids[item.subnet + "_" + item.port]
                    else:
                        s_id = self.createAndAddServiceToHost(
                            h_id,
                            item.service,
                            item.protocol,
                            ports=[str(item.port)]
                        )
                        ids[item.subnet + "_" + item.port] = s_id
                    if web:
                        if item.severity not in self.ignored_severities:
                            v_id = self.createAndAddVulnWebToService(
                                h_id,
                                s_id,
                                item.name,
                                desc=item.description,
                                website=item.host,
                                severity=item.severity,
                                ref=ref,
                                resolution=item.resolution,
                                external_id=f"OPENVAS-{item.id}",
                                data=item.data,
                                cve=cve,
                                cwe=item.cwe,
                                cvss2=cvss2
                            )
                    elif item.severity not in self.ignored_severities:
                        self.createAndAddVulnToService(
                            h_id,
                            s_id,
                            item.name,
                            desc=item.description,
                            severity=item.severity,
                            ref=ref,
                            resolution=item.resolution,
                            external_id=f"OPENVAS-{item.id}",
                            data=item.data,
                            cve=cve,
                            cwe=item.cwe,
                            cvss2=cvss2
                        )
        del parser

    @staticmethod
    def _isIPV4(ip):
        if len(ip.split(".")) == 4:
            return True
        else:
            return False


def createPlugin(*args, **kwargs):
    return OpenvasPlugin(*args, **kwargs)
