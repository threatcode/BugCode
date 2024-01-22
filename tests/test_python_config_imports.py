import unittest


class ImportTests(unittest.TestCase):

    def test_database(self):
        from bugcode.server.config import database
        self.connection_string = database.connection_string

    def test_bugcode_server(self):
        from bugcode.server.config import bugcode_server
        self.bind_address = bugcode_server.bind_address
        self.port = bugcode_server.port
        self.secret_key = bugcode_server.secret_key
        self.websocket_port = bugcode_server.websocket_port

    def test_storage(self):
        from bugcode.server.config import storage
        self.path = storage.path
