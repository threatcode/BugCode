'''
Bugcode Penetration Test IDE
Copyright (C) 2013  Threatcode LLC (http://www.tthreatcode.github.io/bugcode/)
See the file 'doc/LICENSE' for the license information

'''

import pytest


class TestAPIInfoEndpoint:

    def test_api_info_public(self, test_client):
        response = test_client.get('v3/info')
        assert response.status_code == 200
        assert response.json['Bugcode Server'] == 'Running'

    @pytest.mark.usefixtures('logged_user')
    def test_api_info(self, test_client):
        response = test_client.get('v3/info')
        assert response.status_code == 200
        assert response.json['Bugcode Server'] == 'Running'

    def test_api_config_public(self, test_client, session):
        from bugcode import __version__
        response = test_client.get('config')
        assert response.status_code == 200
        assert __version__ in response.json['ver']

    @pytest.mark.usefixtures('logged_user')
    def test_get_config(self, test_client):
        from bugcode import __version__
        res = test_client.get('/config')
        assert res.status_code == 200
        assert __version__ in res.json['ver']
