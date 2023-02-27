import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rpc.rpc_client import *

app = FastAPI()
my_client = RPCClient()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    stuff_read = await file.read()
    response = my_client.upload(filename=file.filename, data=stuff_read)
    return {"info": response.decode()}


@app.get("/downloadfile/{filename}")
async def download_uploaded_file(filename: str):
    file_data = my_client.download(filename)
    return StreamingResponse(
        iter([file_data]),
        headers={
            "Content-Type": "application/octet-stream",
            "Content-Disposition": f"attachment;filename={filename}",
        },
    )


@app.get("/fileslist/")
async def get_list_of_files():
    files_array = my_client.get_list()
    return {"files": files_array}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)
