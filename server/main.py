import shutil # For high level operations on files and collections
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

 

credentials = True
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

#adding cors urls
origins = [
    'http://localhost:3000'
]

# adding middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = credentials,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.post("/helloClient/")
async def testCommunication():
    print("Testing message in Server")
    return {
        "info": f"A client has communicated with server"
    }

@app.post("/uploadfile/")
async def create_upload_file(uploaded_file: UploadFile):
    print("Hello!!!!!!!!")
    file_location = f"/Users/carlosveint/Documents/UploadedFiles559/{uploaded_file.filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object) # first argument is the source, to be copied to second variable (the destination).

    return {
        "info": f"The file '{uploaded_file.filename}' has been successfully uploaded"
    }


@app.get("/downloadfile/")
async def download_uploaded_file(file_name: str):
    file_location = f"/Users/carlosveint/Documents/UploadedFiles559/{file_name}"

    return FileResponse(
        path=file_location, filename=file_name, media_type="application/octet-stream" #To indicate that a body contains arbitrary binary data.
    )


@app.get("/fileslist/")
async def get_list_of_files(file_name: str):
    files_array = os.listdir("/Users/harsh/Documents/UploadedFiles/")
    return {"files": files_array}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
