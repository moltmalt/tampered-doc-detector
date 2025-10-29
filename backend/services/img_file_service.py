import os
import io
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = "gemini-2.5-pro"

genai.configure(api_key=api_key)

def ocr_img(images):
    """
    Extract text from images using Gemini Vision API.
    
    Args:
        images: List of PIL Image objects
        
    Returns:
        str: Concatenated text extracted from all images
    """
    model = genai.GenerativeModel(model_name)
    ocr_texts = ""
    
    prompt = """Extract all text from this image. Return the text exactly as it appears, 
    preserving formatting, line breaks, and spacing as much as possible. 
    If there is no text, return an empty string."""

    for idx, img in enumerate(images):
        try:
            # Convert PIL Image to bytes for Gemini API
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # Generate content with image
            response = model.generate_content([prompt, img])
            
            if response.text:
                ocr_texts += response.text + "\n"
                
        except Exception as e:
            print(f"OCR failed for image {idx + 1}: {e}")
            continue
    
    return ocr_texts.strip()