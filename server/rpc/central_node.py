import rpyc
from rpyc.utils.server import ThreadedServer


class CentralNodeService(rpyc.Service):
    def __init__(self):
        self.connected_replicas = []

    # For accepting a new replica connection
    def exposed_register_replica(self, replica_ip, replica_port):
        self.connected_replicas.append({"ip": replica_ip, "port": replica_port})
        print(
            f"Now we have {len(self.connected_replicas)} replicas connected to central node"
        )

    # We can look into this afterwards, not a core requirement
    # # For finding and disconnection froma given replica
    # def exposed_remove_replica(self, replica_ip):
    #     # Find and disconnect the replica node with the given IP
    #     for replica_conn in self.connected_replicas:
    #         if replica_conn._config["endpoints"][0][0] == replica_ip:
    #             replica_conn.close()
    #             self.connected_replicas.remove(replica_conn)

    # Function to upload a given file
    def exposed_upload_file(self, filename, data):
        # Upload a file to all connected replicas
        for replica in self.connected_replicas:
            replica_conn = rpyc.connect(replica["ip"], replica["port"])
            replica_conn.root.upload_to_replica(filename, data)

        return str.encode(f"The file '{filename}' has been successfully uploaded")

    # Function to upload file with a given filename
    def exposed_download_file(self, filename):
        # If the there are no replicas connected then return nothing
        if len(self.connected_replicas) == 0:
            return ""

        # Otherwise just return it from the first replica in the list
        replica = self.connected_replicas[0]
        replica_conn = rpyc.connect(replica["ip"], replica["port"])
        file_data = replica_conn.root.download_from_replica(filename)
        return file_data

    # Function to get list of all the files on the replicas
    # As for now, data is identical around replicas, we use just the first replica
    def exposed_get_list(self):
        replica = self.connected_replicas[0]
        replica_conn = rpyc.connect(replica["ip"], replica["port"])
        return replica_conn.root.get_list_from_replica()


if __name__ == "__main__":
    # Start the central node server on port 8000
    t = ThreadedServer(CentralNodeService(), port=8000)
    t.start()
