import rpyc
from rpyc.utils.server import ThreadedServer
import os
import hashlib

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
        self.storage_details = {}

    """ code not being used but kept here for future. A missing step regarding deep copy of remote objects has been solved and now should not be a problem.
    def exposed_central_node_died():
        print(f"replica node at port {replica_node_port} is notified for dead central node.\n Reattempt connection")
        while True:
            try:
                print("replica node at port {replica_node_port} Making connection to the central node\n")
                central_node_connection = rpyc.connect(central_node_ip, central_node_port)
                print("replica node at port {replica_node_port} Connection successful\n")
                break
            except Exception:
                import time
                time.sleep(1)
                print(f"replica node at port {replica_node_port} failed connected. reattempting")
                continue
        return "success"
    """

    def exposed_upload_to_replica(self, filename, data):
        print(f"tried to upload yeah {type(filename)}")
        print(filename)
        file_location = self.get_storage_location(filename) + filename

        with open(file_location, "wb+") as f:
            f.write(data)

        file_hash = None
        with open(file_location, "rb") as file:
            contents_stored = file.read()
            # Getting the hash
            file_hash = hashlib.sha256(contents_stored).hexdigest()
        
        self.storage_details[filename] = file_hash # keep track of storage info
        return file_hash

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
    
    def exposed_get_storage_details(self): # returns fields and hashnames key-value pairs
        # return self.storage_details # EFFICIENT RETURN
        # what if replica has file corruptions? Best to read every file in directory and compute hash (INEFFICIENT RETURN)
        # this is an expensive operatoin but later the system can be optimized by switching between EFFICIENT AND INEFFICIENT return on regular interval. This will mantain both stability (can detect issues if a filename is missing or absent or improper hash code if file corrupt) and bandwidth efficiency over time
        print(f"replica received storage details request")
        storage_details = {}
        try:
            files = os.listdir(f"{FOLDER_PATH}")
            print(f"Replica has files {files}")
            for file_name in files:
                # if file is a file and not a fodler
                file_path = os.path.join(FOLDER_PATH, file_name)
                # print(f"\tfilepath is {file_path}")
                file_data = None
                file_hash = None
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    file_hash = hashlib.sha256(file_data).hexdigest()
                storage_details[file_name] = file_hash
            return storage_details # after successful operation
        except:
            print(f"Replica failed giving storage details")
            return self.storage_details # default return value

    def get_storage_location(self, filename: str):
        # Right now just storing at one location
        return self.storage_locations[0]


# The code for connecting the replica with the central node
# goes in here
import sys, os
from dotenv import load_dotenv
import os

# only one of these 2 will end up loading variables
load_dotenv("../.env") # in case python is execute from rpc path
load_dotenv("./.env") # python must be exectured from server path

central_node_ip = os.getenv("CENTRAL_NODE_IP")
central_node_port = int(os.getenv("CENTRAL_NODE_PORT"))

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
