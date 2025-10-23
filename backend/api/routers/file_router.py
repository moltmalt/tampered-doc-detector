from fastapi import APIRouter, File, UploadFile

from services.file_upload_orchestrator import process_upload

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return await process_upload(file)
