import shutil
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(uploaded_file: UploadFile):
    file_location = f"/Users/harsh/Documents/UploadedFiles/{uploaded_file.filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object)

    return {
        "info": f"The file '{uploaded_file.filename}' has been successfully uploaded"
    }
