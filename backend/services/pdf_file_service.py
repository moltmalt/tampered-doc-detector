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

def get_content_streams(file_path):
    file = fitz.open(file_path)
    strams = []

    for page_num, page in enumerate(file, start=1):
        xref = page.get_contents()
        content_bytes = "b"

        if isinstance(xref, list):
            for x in xref:
                content_bytes += file.xref_stream(x)
        else:
            content_bytes = file.xref_stream(xref)
        
        #Done to make the bytes readable by AI
        content_text = content_bytes.decode('latin-1', errors="ignore")
        streams.append({
            "page": page_num,
            "stream": content_text
        })
    
    return streams

def clean_streams(streams, max_chars=5000):
    for s in streams:
        cleaned = s["stream"].replace("\n", " ")
        if len(cleaned) > max_chars:
            cleaned = cleaned[:max_chars] + "..."
        
    return cleaned