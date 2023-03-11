import rpyc
from rpyc.utils.server import ThreadedServer
import os

# May change these variables afterwards
central_node_ip = "localhost"
central_node_port = 8000
replica_node_ip = "localhost"
replica_node_port = 8001


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
            f"{FOLDER_PATH}/" # / added at the end
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
        files_array = os.listdir(f"{FOLDER_PATH}")
        return files_array

    def get_storage_location(self, filename: str):
        # Right now just storing at one location
        return self.storage_locations[0]


# The code for connecting the replica with the central node
# goes in here
import sys, os
if __name__ == "__main__":
    DEFAULT_FOLDER_PATH = "./temp"
    FOLDER_PATH = None
    replica_node_port = None
    if len(sys.argv) < 2:
        print(f"Usage `usage {sys.argv[0]} <PORT> or {sys.argv[0]} <PORT> <STORAGEPATH>")
        exit()
    if len(sys.argv) < 3:
        print(f"Using default folder path: {DEFAULT_FOLDER_PATH}")
        FOLDER_PATH = DEFAULT_FOLDER_PATH
        replica_node_port = int(sys.argv[1])
    else:
        replica_node_port = int(sys.argv[1])
        print(f"Using provided path: {sys.argv[1]}\n\tCorresponding absolute path: {os.path.abspath(sys.argv[2])}")
        FOLDER_PATH = os.path.abspath(sys.argv[2])
    

    print(f"FOLDER PATH IS {FOLDER_PATH}")
    if not os.path.exists(FOLDER_PATH): os.makedirs(FOLDER_PATH)
    print("************ STARTING THE REPLICA PROCESS ***********\n")
    # t = ThreadedServer(ReplicaNodeService(), port=replica_node_port)
    t = ThreadedServer(ReplicaNodeService(), port=replica_node_port)
    t.start()
