import io

# from segmentation import get_segmentator, get_segments
from starlette.responses import Response
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uuid
import os
import shutil

app = FastAPI(
    title="AnimeTransfer image segmentation",
    description="""Anime will not be just anime""",
    version="0.1.0",
)

from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from shutil import copyfile
FINISH_FOLDER_DIR = "finish_processed_files"
UPLOAD_FOLDER_DIR = "uploaded_files"

@app.post("/file/upload/")
async def upload_image_file(file: UploadFile = File(...)):
    if( "image" not in file.content_type) :
        raise HTTPException(status_code=400, detail="Request file bad content type -- need image content_type")
    uuid_var = uuid.uuid4()
    filename = f"{'.'.join(file.filename.split('.')[:-1])}_{uuid_var}.{file.filename.split('.')[-1]}"
    filename = filename.strip()
    file_location = UPLOAD_FOLDER_DIR + "/" + filename
    with open(file_location, "wb") as file_object:
        file_object.write(file.file.read())

    copyfile(file_location, f"{FINISH_FOLDER_DIR}/{filename}")
    return { "filename": filename, "uuid": uuid_var }

@app.get("/file/find_all/")
async def find_files():
    file_list = os.listdir(UPLOAD_FOLDER_DIR)
    finished_file_list = os.listdir(FINISH_FOLDER_DIR)
    status_files = [ "finished" if file in finished_file_list else "not-finished" for file in file_list ]
    return [ { "file": file_list[i] , "status": status_files[i] } for i in range(len(file_list))]

@app.get("/file/delete/")
async def delete_file(filename: str) :
    os.remove(UPLOAD_FOLDER_DIR + "/" + filename)

@app.get("/file/download_finished/")
async def download_finished_files(filename: str):
    finish_processed_files = os.listdir('finish_processed_files')
    print(finish_processed_files)
    print(filename)
    print(filename in finish_processed_files)
    if filename not in finish_processed_files :
        raise HTTPException(status_code=400, detail="Error, file not finished")
    return FileResponse(path=f"finish_processed_files/{filename}")

# async def get_status()



