import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import time


is_backup = False
PRIMARY_CENTRAL_NODE_PORT = 8000
BACKUP_CENTRAL_NODE_PORT = 8050


class CentralNodeService(rpyc.Service):
    def __init__(self, replica_info):
        if replica_info is None:
            self.connected_replicas = []
            self.new_replicas = []
            self.leader_details = { "ip": None, "port": None }
        else:
            self.connected_replicas = replica_info[0]
            self.new_replicas = replica_info[1]
            self.leader_details = replica_info[2]

        self.check_replicas_thread = threading.Thread(target=self.check_replicas, daemon=True)
        self.check_replicas_thread.start()

    # For accepting a new replica connection
    def exposed_register_replica(self, replica_ip, replica_port):
        print("Central node detects a replica connecting from port", replica_port)
        self.connected_replicas.append({"ip": replica_ip, "port": replica_port})
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
        # Upload a file to all connected replicas
        for replica in self.connected_replicas:
            print("Central node sending to replica port", replica["port"])
            replica_conn = rpyc.connect(replica["ip"], replica["port"])
            replica_conn.root.upload_to_replica(filename, data)

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

    def exposed_get_replica_details(self):
        return [self.connected_replicas, self.new_replicas, self.leader_details]

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
                new_replica_conn.root.upload_to_replica(file, file_data)

            self.new_replicas.remove(new_replica)
            print("Copying finished")


    def check_replicas(self):
        central_node_stuff = None
        while True:
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
        self.running = True
        self.central_node_stuff = None
        while self.running:
            try:
                print("Primary central still running")
                conn = rpyc.connect("localhost", PRIMARY_CENTRAL_NODE_PORT)
                self.central_node_stuff = conn.root.get_replica_details()
                print(self.central_node_stuff)
                conn.close()
            except ConnectionRefusedError:
                print("Primary central node not running, starting backup central node")
                backup_server = ThreadedServer(CentralNodeService(replica_info=self.central_node_stuff), port=PRIMARY_CENTRAL_NODE_PORT)
                backup_server.start()
                break
            time.sleep(1)

    def stop(self):
        self.running = False



if __name__ == "__main__":
    # Start the central node server on port 8000
        is_backup = True

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

            primary_node = ThreadedServer(CentralNodeService(replica_info=None), port=8000)
            primary_node.start()
