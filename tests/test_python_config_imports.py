import unittest


class ImportTests(unittest.TestCase):

    def test_database(self):
        from bogcode.server.config import database
        self.connection_string = database.connection_string

    def test_bogcode_server(self):
        from bogcode.server.config import bogcode_server
        self.bind_address = bogcode_server.bind_address
        self.port = bogcode_server.port
        self.secret_key = bogcode_server.secret_key
        self.websocket_port = bogcode_server.websocket_port

    def test_storage(self):
        from bogcode.server.config import storage
        self.path = storage.path
