import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import time
import subprocess

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

    # def exposed_get_replica_details(self):
    #     return {
    #         "connected_replicas":  self.connected_replicas,
    #         "new_replicas": self.new_replicas,
    #         "leader_details": self.leader_details
    #     }

    def exposed_get_replica_details(self):
        return self.connected_replicas
    
    def exposed_set_replica_details(self, connected_replicas):
        self.connected_replicas = connected_replicas
        return "success"
    
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
            # print("central node the replicas connecte are ", self.connected_replicas)
            # time.sleep(2)
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
                # self.central_node_stuff = conn.root.get_replica_details()
                conn.close() # if array is accesed after closing or having lost connection and not deep copied -> ERROR
                try:
                    print(type(self.central_node_stuff))
                    print(self.central_node_stuff) # this is the source of bug
                except Exception:
                    print("List failing to print")
            except ConnectionRefusedError:
                print("Primary central node not running, backup node TAKING OVER as central node")
                # issue: executing a ThreadedServer inside a ThreadedServer may be causing unexpected behaviour -> not sure about its
                # maybe Threadserver in Threadserver is completely fine. However, issue could be the fact that array self.central_node_stuff was not DEEP COPIED!
                backup_server = ThreadedServer(CentralNodeService(self.central_node_stuff), port=PRIMARY_CENTRAL_NODE_PORT)
                backup_server.start()

                # subprocess fix not needed anymore as issue has been fixed
                # rather create a new process to re-run central node on SAME port (create a new process without waiting)
                # time.sleep(1)
                # subprocess.Popen(['python3', f"{sys.argv[0]}", 'false']) # run same file (with arg false -- which means run it as central node and not as backup)
                
                # MAX_ATTEMPTS = 5 # SOLUTION1: send connected replicas to central node -> not needed anymore. ojbect passed in constructor
                # while MAX_ATTEMPTS:
                #     time.sleep(2) # allow 2 seconds for central node to be setup again
                #     if self.send_stuff_to_central_node(): break
                #     MAX_ATTEMPTS -= 1

                # try: # SOLUTION2: notify replicas to reconnect to central node -> not needed anymore for same reason.
                #     arr= self.central_node_stuff
                #     print("Arrays is ", arr) # uncomment this and above line. It will crash.
                # except Exception:
                #     input("Something wrong happened")
                # for replica in self.central_node_stuff:
                #     print("Backup node notifying replica", replica, "for restarting central ndoe")
                #     replica_conn = rpyc.connect(replica["ip"], replica["port"])
                #     replica_conn.close()
            except Exception:
                print("Some other error occured!")

            time.sleep(1)

    """
    not needed anymore but here for future pruposes
    def send_stuff_to_central_node(self):
        try:
            connection = rpyc.connect("localhost", PRIMARY_CENTRAL_NODE_PORT)
            print("Connection established")
            arr = self.central_node_stuff if self.central_node_stuff is not None else []
            response = connection.root.set_replica_details(arr)
            print("Backup node successfully sent stuff to central node. Here the response")
            print(response)
            connection.close()
            time.sleep(1)
            return True
        except Exception:
            print("Backup node failed to send stuff to central node")
            return False
    """


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
