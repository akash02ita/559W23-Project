import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import time


class CentralNodeService(rpyc.Service):
    def __init__(self):
        self.connected_replicas = []
        self.leader_details = { "ip": None, "port": None }
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

    # Function for leader election
    def elect_new_leader(self):
        print("Trying to elect a new leader")

        if (len(self.connected_replicas)>0):
            self.leader_details = self.connected_replicas[0]
            print(f"Successfully elected a new leader with details {self.leader_details}")
        else:
            self.leader_details = None
            print("No replica connected. Unable to elect a new leader.")

    def check_replicas(self):
        while True:
            if self.leader_details not in self.connected_replicas and len(self.connected_replicas)>0:
                # If the leader replica is not connected, elect a new leader
                print("Looks like the leader replica got removed")
                self.elect_new_leader()
            
            for replica in self.connected_replicas:
                try:
                    replica_conn = rpyc.connect(replica["ip"], replica["port"])
                    replica_conn.ping()
                except:
                    print(f"Replica {replica['ip']}:{replica['port']} is not respoding. Removing it.")
                    self.connected_replicas.remove(replica)
                    print(f"Number of connected replicas is:", len(self.connected_replicas))
            time.sleep(2)


if __name__ == "__main__":
    # Start the central node server on port 8000
    t = ThreadedServer(CentralNodeService(), port=8000)
    t.start()
