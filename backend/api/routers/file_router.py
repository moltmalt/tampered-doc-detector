from fastapi import APIRouter, File, UploadFile

from services.file_service import save_file

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return await save_file(file)