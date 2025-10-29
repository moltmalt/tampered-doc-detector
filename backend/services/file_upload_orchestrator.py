import json

from fastapi import File, UploadFile

from .crud_file_service import save_file
from .text_analysis_service import evaluate_embeddings_and_ocr
from .business_logic import file_format_checker, clean_json_response
from .ai_analysis_service import analyze_embeddings_ocr_with_gemini, analyze_content_streams_with_gemini
from .pdf_file_service import get_embedded_pdf_text, convert_pdf_to_image, get_content_streams
from .img_file_service import ocr_img

async def process_upload(file: UploadFile):
    message = await save_file(file)
    file_path = message["file_path"]
    analysis_result = {}

    images = convert_pdf_to_image(file_path)
    embedded_texts = get_embedded_pdf_text(file_path)
    ocr_texts = ocr_img(images)

    math_analysis_result = embeddings_ocr_subprocess(
        analysis_result, 
        file_path, 
        embedded_texts, 
        ocr_texts
        )
    
    analysis = math_analysis_result.get("math_analysis", {}).get("analysis", {})
    cosine_score = analysis.get("cosine_similarity_score")
    sequence_score = analysis.get("sequence_similarity_score")

    if cosine_score < 0.9 or sequence_score < 0.95:
        embeddings_ocr_gemini_result_text = analyze_embeddings_ocr_with_gemini_subprocess(
            analysis_result,
            embedded_texts,
            ocr_texts
            )

    content_streams_ai_inputs = get_content_streams(file_path)
    
    analyze_content_streams_with_gemini_subprocess(
        analysis_result,
        content_streams_ai_inputs
        )

    return analysis_result


def embeddings_ocr_subprocess(analysis_result, file_path, embedded_texts, ocr_texts):
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
    return analysis_result


def analyze_embeddings_ocr_with_gemini_subprocess(analysis_result, embedded_texts, ocr_texts):
    try:
        embeddings_ocr_gemini_result_text = analyze_embeddings_ocr_with_gemini(
            embedded_texts,
            ocr_texts
        )
        
        cleaned_result = clean_json_response(embeddings_ocr_gemini_result_text)
        gemini_analysis = json.loads(cleaned_result)
        analysis_result["embedded_text_ai_analysis"] = gemini_analysis
            
    except Exception as e:
        print(f"Gemini analysis failed: {e}")
        analysis_result["embedded_text_ai_analysis"] = None
        analysis_result["embedded_text_ai_analysis_error"] = str(e)
    
    return analysis_result

def analyze_content_streams_with_gemini_subprocess(analysis_result, content_streams_ai_inputs):
    try:
        content_streams_gemini_result_text = analyze_content_streams_with_gemini(
            content_streams_ai_inputs
        )

        parsed_results = []
        for result in content_streams_gemini_result_text:
            parsed_analysis = json.loads(result["analysis"])

            parsed_results.append({
                "page": result["page"],
                "analysis": parsed_analysis,
                "is_suspicious": parsed_analysis.get("modified") in ["true", "unsure"],
                "confidence": parsed_analysis.get("confidence", 0)
            })
        analysis_result["content_streams_ai_analysis"] = parsed_results
        suspicious_pages = [r for r in parsed_results if r["is_suspicious"]]
        analysis_result["content_streams_summary"] = {
            "total_pages": len(parsed_results),
            "suspicious_pages": len(suspicious_pages),
            "suspicious_page_numbers": [r["page"] for r in suspicious_pages]
        }
    except Exception as e:
        print(f"Gemini analysis failed: {e}")
        analysis_result["content_streams_ai_analysis"] = None
        analysis_result["content_streams_ai_analysis_error"] = str(e)
    
    return analysis_result
