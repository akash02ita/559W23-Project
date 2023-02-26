import os
import shutil
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(uploaded_file: UploadFile):
    file_location = f"/Users/harsh/Documents/UploadedFiles/{uploaded_file.filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object)

    return {
        "info": f"The file '{uploaded_file.filename}' has been successfully uploaded"
    }


@app.get("/downloadfile/")
async def download_uploaded_file(file_name: str):
    file_location = f"/Users/harsh/Documents/UploadedFiles/{file_name}"

    return FileResponse(
        path=file_location, filename=file_name, media_type="application/octet-stream"
    )


@app.get("/fileslist/")
async def get_list_of_files(file_name: str):
    files_array = os.listdir("/Users/harsh/Documents/UploadedFiles/")
    return {"files": files_array}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
