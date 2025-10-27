import json

from fastapi import File, UploadFile

from .crud_file_service import save_file
from .text_analysis_service import evaluate_embeddings_and_ocr
from .business_logic import file_format_checker
from .ai_analysis_service import analyze_embeddings_ocr_with_gemini
from .pdf_file_service import get_embedded_pdf_text, convert_pdf_to_image
from .img_file_service import ocr_img

async def process_upload(file: UploadFile):

    message = await save_file(file)
    file_path = message["file_path"]
    analysis_result = {

    }

    images = convert_pdf_to_image(file_path)
    embedded_texts = get_embedded_pdf_text(file_path)
    ocr_texts = ocr_img(images)

    # First Phase
    try:
        math_analysis_result = evaluate_embeddings_and_ocr(
            file_path,
            embedded_texts,
            ocr_texts
            )
        analysis_result["math_analysis"] = math_analysis_result
    except Exception as e:
        print(f"Analysis failed:{e}")
        return{
            "error":"Analysis failed",
            "message": str(e)
        }
    
    print(math_analysis_result)
    
    analysis = math_analysis_result.get("analysis", {})
    cosine_score = analysis.get("cosine_similarity_score")
    sequence_score = analysis.get("sequence_similarity_score")

    if cosine_score < 0.9 or sequence_score < 0.95:
        # Second Phase 
        try:
            gemini_result_text = analyze_embeddings_ocr_with_gemini(
                embedded_texts,
                ocr_texts
            )
            print(f"Raw Gemini response: {gemini_result_text}")
            
            gemini_analysis = json.loads(gemini_result_text)
            analysis_result["ai_analysis"] = gemini_analysis
            
        except Exception as e:
            print(f"Gemini analysis failed: {e}")
            analysis_result["ai_analysis"] = None
            analysis_result["ai_analysis_error"] = str(e)
    
    return analysis_result
