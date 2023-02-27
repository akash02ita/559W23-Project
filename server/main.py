import shutil # For high level operations on files and collections
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

import os
import sys
 

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
    file_location = f"{FOLDER_PATH}/{uploaded_file.filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object) # first argument is the source, to be copied to second variable (the destination).

    return {
        "info": f"The file '{uploaded_file.filename}' has been successfully uploaded"
    }


@app.get("/downloadfile/")
async def download_uploaded_file(file_name: str):
    file_location = f"{FOLDER_PATH}/{file_name}"

    return FileResponse(
        path=file_location, filename=file_name, media_type="application/octet-stream" #To indicate that a body contains arbitrary binary data.
    )


@app.get("/fileslist/")
# async def get_list_of_files(file_name: str):
async def get_list_of_files(): # there should be no list of files
    files_array = os.listdir(f"{FOLDER_PATH}")
    return {"files": files_array}


DEFAULT_FOLDER_PATH = "./temp"
FOLDER_PATH = None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Using default folder path: {DEFAULT_FOLDER_PATH}")
        FOLDER_PATH = DEFAULT_FOLDER_PATH
    else:
        print(f"Using provided path: {sys.argv[1]}\n\tCorresponding absolute path: {os.path.abspath(sys.argv[1])}")
        FOLDER_PATH = os.path.abspath(sys.argv[1])
    

    print(f"FOLDER PATH IS {FOLDER_PATH}")
    if not os.path.exists(FOLDER_PATH): os.makedirs(FOLDER_PATH)

    uvicorn.run(app, host="127.0.0.1", port=8000)
