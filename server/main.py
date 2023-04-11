import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import rpyc

credentials = True
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

#adding cors urls
origins = [
    #'http://localhost:3000'
    "*" # allow everything
]

# adding middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = credentials,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


# We can change this afterwards when deploying
central_node_ip = "localhost"
central_node_port = 8000
# central_node_conn = rpyc.connect(central_node_ip, central_node_port)


@app.post("/uploadfile/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    stuff_read = await uploaded_file.read()
    central_node_conn = rpyc.connect(central_node_ip, central_node_port)
    response = central_node_conn.root.upload_file(
        filename=uploaded_file.filename, 
        data=stuff_read
    )
    # central_node_conn.close() # for now no connection closure
    return {"info": response.decode()}


@app.get("/downloadfile/{filename}")
async def download_uploaded_file(filename: str):
    central_node_conn = rpyc.connect(central_node_ip, central_node_port)
    file_data = central_node_conn.root.download_file(filename)
    # central_node_conn.close()
    return StreamingResponse(
        iter([file_data]),
        headers={
            "Content-Type": "application/octet-stream",
            "Content-Disposition": f"attachment;filename={filename}",
        },
    )


@app.get("/fileslist/")
async def get_list_of_files():
    central_node_conn = rpyc.connect(central_node_ip, central_node_port)
    files_array = central_node_conn.root.get_list()
    # central_node_conn.close() # must deep copy stuff before closing. for now no connectin closure
    return {"files": files_array}


import socket
from socket import gethostbyname
from socket import gethostname
port = 9000
if __name__ == "__main__":
    ip = gethostbyname(gethostname())
    print(f"Use the link: http://{ip}:{port}")
    print(f"Api Swagger at: http://{ip}:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)
