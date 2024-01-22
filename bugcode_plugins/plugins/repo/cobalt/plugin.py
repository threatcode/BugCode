"""
Bugcode Penetration Test IDE
Copyright (C) 2013  KhulnaSoft Ltd (http://www.khulnasoft.com/)
See the file 'doc/LICENSE' for the license information

"""

from bugcode_plugins.plugins.plugin import PluginCSVFormat
from urllib.parse import urlparse
import csv
import io
from dateutil.parser import parse



__author__ = "Blas"
__copyright__ = "Copyright (c) 2019, KhulnaSoft Ltd"
__credits__ = ["Blas"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Blas"
__email__ = "bmoyano@khulnasoft.com"
__status__ = "Development"



class CobaltParser:
    """
    The objective of this class is to parse an CSV file generated by the Cobalt tool.

    TODO: Handle errors.
    TODO: Test Cobalt output version. Handle what happens if the parser doesn't support it.
    TODO: Test cases.

    @param Cobalt_filepath A proper simple report generated by Cobalt
    """
    def __init__(self, output):

        reader = csv.DictReader(io.StringIO(output))
        self.headers = reader.fieldnames
        self.rows = []
        for row in reader:
            for k, v in row.items():
                if v.startswith("'"):
                    row[k] = v[1:]
            self.rows.append(row)


class CobaltPlugin(PluginCSVFormat):
    """
    Example plugin to parse Cobalt output.
    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.csv_headers = [{'Token'}, {'Tag'}]
        self.id = "Cobalt"
        self.name = "Cobalt CSV Output Plugin"
        self.plugin_version = "0.0.1"
        self.version = "0.0.1"
        self.framework_version = "1.0.1"

    def parseOutputString(self, output):
        try:
            parser = CobaltParser(output)
        except:
            print("Error parser output")
            return None

        for row in parser.rows:
            url = row['BrowserUrl']
            if not url:
                continue
            url_data = urlparse(url)
            scheme = url_data.scheme
            port = url_data.port
            try:
                run_date = parse(row['CreatedAt'])
            except:
                run_date = None
            if url_data.port is None:
                if scheme == 'https':
                    port = 443
                elif scheme == 'http':
                    port = 80
            else:
                port = url_data.port
            name = self.resolve_hostname(url_data.netloc)
            references = []
            if row['RefKey']:
                references.append(row['RefKey'])
            if row['ResearcherUrl']:
                references.append(row['ResearcherUrl'])
            references.append(row['ReportUrl'])
            request = row['HttpRequest'] if row['HttpRequest'] else row['BrowserUrl']
            h_id = self.createAndAddHost(name=name, hostnames=[url_data.netloc])
            s_id = self.createAndAddServiceToHost(h_id, scheme, "tcp", ports=port, status="open")
            self.createAndAddVulnWebToService(h_id, s_id, name=row['Title'], desc=row['Description'],
                                              ref=references, resolution=row['SuggestedFix'],
                                              website=url_data.netloc, request=request,
                                              pname=url_data.params, category=row['Type'], path=url_data.path,
                                              data=row['StepsToReproduce'], external_id=row['Tag'], run_date=run_date)


def createPlugin(*args, **kwargs):
    return CobaltPlugin(*args, **kwargs)