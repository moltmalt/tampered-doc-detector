import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = "gemini-2.5-pro"

genai.configure(api_key=api_key)


def analyze_embeddings_ocr_with_gemini(embedded_texts, ocr_texts):
    model = genai.GenerativeModel(model_name)

    prompt = f"""
    You are a forensic text analysis AI specializing in detecting document tampering. 
    Compare the following two text variations of the same document:

    Embedded text from PDF source:
    {embedded_texts}

    OCR texts from rendered image/s:
    {ocr_texts}

    Instructions:
    
    Identify if the differences suggest intentional tampering or just OCR noise. Limit observations 
    document tampering detection.
    Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks):
    {{
        "tampering_suspected": "true or false or unsure",
        "confidence": 85,
        "summary": "brief explanation of findings",
        "notable_differences": ["difference 1", "difference 2"]
    }}
    """

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    return response.text

def analyze_content_streams_with_gemini(content_streams_ai_inputs):
    model = genai.GenerativeModel(model_name)
    results = []
    
    for item in content_streams_ai_inputs:
        response = model.generate_content(
            item["prompt"],
            generation_config={"response_mime_type": "application/json"}
            )

        results.append({
            "page": item["page"],
            "analysis": response.text
        })

    return results

def remove_null_from_simplified_stream(content_stream):
    for b in content_stream:
        b["text"] = b["text"].replace("\u0000", "")
    
    return content_stream