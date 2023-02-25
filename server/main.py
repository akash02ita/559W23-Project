import shutil
import uvicorn
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
