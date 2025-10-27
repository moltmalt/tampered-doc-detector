import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)


def analyze_embeddings_ocr_with_gemini(embedded_texts, ocr_texts):
    model = genai.GenerativeModel("gemini-2.5-pro")

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