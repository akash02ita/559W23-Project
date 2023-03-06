import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import rpyc

app = FastAPI()

# We can change this afterwards when deploying
central_node_ip = "localhost"
central_node_port = 8000
central_node_conn = rpyc.connect(central_node_ip, central_node_port)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    stuff_read = await file.read()
    response = central_node_conn.root.upload_file(
        filename=file.filename, data=stuff_read
    )
    return {"info": response.decode()}


@app.get("/downloadfile/{filename}")
async def download_uploaded_file(filename: str):
    file_data = central_node_conn.root.download_file(filename)
    return StreamingResponse(
        iter([file_data]),
        headers={
            "Content-Type": "application/octet-stream",
            "Content-Disposition": f"attachment;filename={filename}",
        },
    )


@app.get("/fileslist/")
async def get_list_of_files():
    files_array = central_node_conn.root.get_list()
    return {"files": files_array}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)
