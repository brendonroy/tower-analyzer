from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Pinwheel API is running!"}

@app.post("/upload/")
async def upload_photos(
    files: List[UploadFile] = File(...),
    gps: str = Form(...),
    azimuth: str = Form(...),
):
    saved_files = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)

    return {
        "saved_files": saved_files,
        "gps": gps,
        "azimuth": azimuth
    }

#  ADD THESE TWO NEW ROUTES BELOW:

@app.get("/photos/")
def list_photos():
    files = []
    for filename in os.listdir(UPLOAD_DIR):
        path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(path):
            files.append(filename)
    return {"photos": files}

@app.get("/photos/{filename}")
def get_photo(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
