import os
from core.config import UPLOAD_DIRECTORY

# this file should ONLY accept file paths

async def save_file_to_storage(save_path, content):
    with open(save_path, "wb") as f:
        f.write(content)

    return {
        "status": True,
        "filename": os.path.basename(save_path)
    }

def get_file(file_path):
    file_exists = os.path.exists(file_path)

    if file_exists:
        return {
                "status": True,
                "filename": filename
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