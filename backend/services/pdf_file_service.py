from core.config import POPPLER_PATH

from pdf2image import convert_from_path
from pdfminer.high_level import extract_text

def convert_pdf_to_image(file_path):
    images = convert_from_path(
        file_path, 
        dpi=300, 
        fmt="png",
        poppler_path = POPPLER_PATH
        )
    return images

def get_embedded_pdf_text(file_path):
    embedded_text = extract_text(file_path)
    return embedded_text