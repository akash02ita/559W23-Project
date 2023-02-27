import rpyc
from rpyc.utils.server import ThreadedServer
import os


class FastAPIServer(rpyc.Service):
    def __init__(self):
        self.storage_locations = [
            "/Users/harsh/Documents/UploadedFilesNode1/",
            "/Users/harsh/Documents/UploadedFilesNode2/",
        ]

    def exposed_upload(self, filename, data):
        print(f"tried to upload yeah {type(filename)}")
        print(filename)
        file_location = self.get_storage_location(filename) + filename

        with open(file_location, "wb+") as f:
            f.write(data)

        return str.encode(f"The file '{filename}' has been successfully uploaded")

    def exposed_download(self, filename: str):
        file_location = self.get_storage_location(filename) + filename
        with open(file_location, "rb") as f:
            file_data = f.read()
        return file_data

    def exposed_get_list(self):
        files_array = os.listdir("/Users/harsh/Documents/UploadedFilesNode1/")
        return files_array

    def get_storage_location(self, filename: str):
        # Right now just storing at one location
        return self.storage_locations[0]


if __name__ == "__main__":
    t = ThreadedServer(FastAPIServer, port=8002)
    t.start()
