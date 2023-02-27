import rpyc


class RPCClient:
    def __init__(self):
        self.conn = rpyc.connect("localhost", 8002)

    def upload(self, filename, data):
        return self.conn.root.upload(filename, data)

    def download(self, filename):
        return self.conn.root.download(filename)

    def get_list(self):
        return self.conn.root.get_list()
