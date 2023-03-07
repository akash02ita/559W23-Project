import rpyc
from rpyc.utils.server import ThreadedServer
import os

# May change these variables afterwards
central_node_ip = "localhost"
central_node_port = 8000
replica_node_ip = "localhost"
replica_node_port = 8002


class ReplicaNodeService(rpyc.Service):
    def __init__(self):
        super().__init__()

        print("Making connection to the central node\n")
        central_node_connection = rpyc.connect(central_node_ip, central_node_port)
        print("Connection successful\n")

        # This calls the function at the central node for accepting replica connection
        print("Sending replica info to the central node")
        central_node_connection.root.register_replica(
            replica_node_ip, replica_node_port
        )
        print("Replica info successfully sent\n")

        self.storage_locations = [
            "/Users/harsh/Documents/UploadedFilesNode1/",
            "/Users/harsh/Documents/UploadedFilesNode2/",
        ]

    def exposed_upload_to_replica(self, filename, data):
        print(f"tried to upload yeah {type(filename)}")
        print(filename)
        file_location = self.get_storage_location(filename) + filename

        with open(file_location, "wb+") as f:
            f.write(data)

        return str.encode(f"The file '{filename}' has been successfully uploaded")

    def exposed_download_from_replica(self, filename: str):
        file_location = self.get_storage_location(filename) + filename

        try:
            with open(file_location, "rb") as f:
                file_data = f.read()
            return file_data
        except:
            return None

    def exposed_get_list_from_replica(self):
        files_array = os.listdir("/Users/harsh/Documents/UploadedFilesNode2/")
        return files_array

    def get_storage_location(self, filename: str):
        # Right now just storing at one location
        return self.storage_locations[1]


# The code for connecting the replica with the central node
# goes in here
if __name__ == "__main__":

    print("************ STARTING THE REPLICA PROCESS ***********\n")
    t = ThreadedServer(ReplicaNodeService(), port=replica_node_port)
    t.start()
