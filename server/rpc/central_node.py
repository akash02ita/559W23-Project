import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import time
import hashlib

is_backup = False
PRIMARY_CENTRAL_NODE_PORT = 8000
BACKUP_CENTRAL_NODE_PORT = 8050

class CentralNodeService(rpyc.Service):
    def __init__(self, existing_replicas = []):
        print(f"existing replicas are {existing_replicas}")
        self.connected_replicas = existing_replicas
        self.new_replicas = []
        self.leader_details = { "ip": None, "port": None }

        self.check_replicas_thread = threading.Thread(target=self.check_replicas, daemon=True)
        self.check_replicas_thread.start()
        self.critical_sections_filenames = {}

    def acquire_filename_lock(self, fname: str):
        if fname not in self.critical_sections_filenames:
            self.critical_sections_filenames[fname] = threading.Lock()
        self.critical_sections_filenames[fname].acquire(blocking=True)
        return True
    def release_filename_lock(self, fname: str):
        if fname in self.critical_sections_filenames:
            self.critical_sections_filenames[fname].release()
        return True

    # For accepting a new replica connection
    def exposed_register_replica(self, replica_ip, replica_port):
        print("Central node detects a replica connecting from port", replica_port, replica_ip)
        self.connected_replicas.append({"ip": "localhost", "port": replica_port})
        print(
            f"Now we have {len(self.connected_replicas)} replicas connected to central node"
        )

        # Whenever we have the first connection 
        # It's automatically chosen as the leader
        if len(self.connected_replicas) == 1:
            self.elect_new_leader()
        # It means it's a replica after the first one has connected
        else:
            self.new_replicas.append({"ip": replica_ip, "port": replica_port})


    # Function to upload a given file
    def exposed_upload_file(self, filename, data):
        # First get the hash of data that we need to store on replicas
        # Getting the hash
        file_sha = hashlib.sha256(data).hexdigest()
        print('The file sha is ', file_sha)

        print(f"Acquiring lock for file {filename}. Sha is {file_sha}")
        self.acquire_filename_lock(filename)
        print(f"Lock to file {filename} acquired successfully. Sha is {file_sha}")

        print("Uploading the file from central node to all the connected replicas")
        # Upload a file to all connected replicas
        for replica in self.connected_replicas:
            print("Central node sending to replica port", replica["port"])
            replica_conn = rpyc.connect(replica["ip"], replica["port"])
            while True:
                try:
                    replica_response = replica_conn.root.upload_to_replica(filename, data)
                    print("the replica response is ", replica_response)
                except Exception:
                    print("Failed to upload the file this time")
                
                # If the hashes match (this means that copying has been done correctly)
                # i.e. consistency has been ensured
                if replica_response == file_sha:
                    break

        print(f"Releasing lock for file {filename}. Sha is {file_sha}")
        self.release_filename_lock(filename)
        print(f"Released successfuly lock for file {filename}. Sha is {file_sha}")
        
        return str.encode(f"The file '{filename}' has been successfully uploaded")

    # Function to upload file with a given filename
    def exposed_download_file(self, filename):
        # If the there are no replicas connected then return nothing
        if len(self.connected_replicas) == 0:
            return ""

        # Otherwise just return it from the leader replica
        replica = self.leader_details
        replica_conn = rpyc.connect(replica["ip"], replica["port"])
        file_data = replica_conn.root.download_from_replica(filename)
        return file_data

    # Function to get list of all the files on the replicas
    # As for now, data is identical around replicas, we use just use the leader replica
    def exposed_get_list(self):
        replica = self.leader_details
        replica_conn = rpyc.connect(replica["ip"], replica["port"])
        return replica_conn.root.get_list_from_replica()


    # TODO: add the new_replicas info too here
    def exposed_get_replica_details(self):
        return self.connected_replicas
    
    
    # Function for leader election
    def elect_new_leader(self):
        print("Trying to elect a new leader")

        if (len(self.connected_replicas)>0):
            self.leader_details = self.connected_replicas[0]
            print(f"Successfully elected a new leader with details {self.leader_details}")
        else:
            self.leader_details = None
            print("No replica connected. Unable to elect a new leader.")


    def copy_stuff_to_new_replicas(self):

        for new_replica in self.new_replicas:
                
            # This means it's some new replica connecting
            # Just copy all of leader replica stuff to it
            print("Copying data to the newly connected replica from leader")
            leader_info = self.leader_details
            leader_conn = rpyc.connect(leader_info["ip"], leader_info["port"])
            new_replica_conn = rpyc.connect(new_replica["ip"], new_replica["port"])
            
            list_of_files = leader_conn.root.get_list_from_replica()
            for file in list_of_files:
                file_data = leader_conn.root.download_from_replica(file)

                file_sha = hashlib.sha256(file_data).hexdigest()
                print('The file sha is ', file_sha)

                while True:
                    try:
                        new_replica_response = new_replica_conn.root.upload_to_replica(file, file_data)
                        print("the new replica response is ", new_replica_response)
                    except Exception:
                        print("Failed to upload the file to new_replica this time")
                
                    # If the hashes match (this means that copying has been done correctly)
                    # i.e. consistency has been ensured
                    if new_replica_response == file_sha:
                        break
                

            self.new_replicas.remove(new_replica)
            print("Copying finished")


    def check_replicas(self):
        central_node_stuff = None
        while True:
            if self.connected_replicas is None: continue
            if len(self.connected_replicas) == 0: continue
            if self.leader_details not in self.connected_replicas and len(self.connected_replicas)>0:
                # If the leader replica is not connected, elect a new leader
                print("Looks like the leader replica got removed")
                self.elect_new_leader()
            
            self.copy_stuff_to_new_replicas()

            for replica in self.connected_replicas:
                try:
                    replica_conn = rpyc.connect(replica["ip"], replica["port"])
                    replica_conn.ping()
                except:
                    print(f"Replica {replica['ip']}:{replica['port']} is not respoding. Removing it.")
                    self.connected_replicas.remove(replica)
                    print(f"Number of connected replicas is:", len(self.connected_replicas))
            time.sleep(2)

class BackupCentralNode(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = False

    def run(self):
        def ultra_deep_copy(remote_object_of_list_of_dic):
            temp = [x for x in remote_object_of_list_of_dic]
            temp2 = [{'ip': x['ip'], 'port': x['port']} for x in temp] # must fully deep copy everything!
            return temp2
        
        self.running = True
        self.central_node_stuff = None
        while self.running:
            try:
                print("Primary central still running")
                conn = rpyc.connect("localhost", PRIMARY_CENTRAL_NODE_PORT)
                try:
                    temp = conn.root.get_replica_details()
                    self.central_node_stuff = ultra_deep_copy(temp) # immediately deep copy as in rpyc, temp does not contain the array data until accessed
                    print(self.central_node_stuff)
                except Exception:
                    print("Connected replicas fetch list failing")
                conn.close() # if array is accesed after closing or having lost connection and not deep copied -> ERROR
                try:
                    print(type(self.central_node_stuff))
                    print(self.central_node_stuff) # this is the source of bug
                except Exception:
                    print("List failing to print")
            except ConnectionRefusedError:
                print("Primary central node not running, backup node TAKING OVER as central node")
                backup_server = ThreadedServer(CentralNodeService(self.central_node_stuff), port=PRIMARY_CENTRAL_NODE_PORT)
                backup_server.start()
            except Exception:
                print("Some other error occured!")

            time.sleep(1)

    def stop(self):
        self.running = False


import sys
if __name__ == "__main__":
    # Start the central node server on port 8000
        is_backup = False
        if len(sys.argv) >= 2:
            is_backup = sys.argv[1].lower() == "true"

        if is_backup:
            print("works")
            backup_node = BackupCentralNode()
            backup_node.start()

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                backup_node.stop

        else:

            primary_node = ThreadedServer(CentralNodeService(), port=PRIMARY_CENTRAL_NODE_PORT)
            primary_node.start()
