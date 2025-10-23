import os
from core.config import UPLOAD_DIRECTORY
from .os_funcs import get_filename_from_path

# this file should ONLY accept file paths and file contents

async def save_file_to_storage(save_path, content):
    with open(save_path, "wb") as f:
        f.write(content)

    return {
        "status": True,
        "filename": get_filename_from_path(save_path),
        "file_path": save_path
    }

def get_file(file_path):
    file_exists = os.path.exists(file_path)

    if file_exists:
        return {
                "status": True,
                "filename": get_filename_from_path(file_path)
            }
        
    return{
        "status": False
    }
    
"""from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/upload")
async def save(file: UploadFile = File(...)):
    allowed_types = ["applciation/pdf", "image/jpeg", "image/png"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed types are PDF, JPEG and PNG."
        )
    
    content = await file.read()

    with open(file.filename, wb) as f:
        f.write(content)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(content)
    }
"""