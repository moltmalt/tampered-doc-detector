from fastapi import File, UploadFile

from .crud_file_service import save_file
from .text_analysis_service import evaluate_embeddings_and_ocr

async def process_upload(file: UploadFile):

    message = await save_file(file)

    analysis_result = None

    try:
        analysis_result = evaluate_embeddings_and_ocr(
            message["file_path"]
            )
    except Exception as e:
        print(f"Analysis failed:{e}")
    
    return build_analysis_response(analysis_result)

def build_analysis_response(analysis_result):
    response = {

    }

    if analysis_result:
        response["analysis"] = analysis_result
    else:
        response["analysis"] = None
        response["message"] = "File uploaded but analysis was not performed"
        
    return response