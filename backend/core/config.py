import os
import shutil

UPLOAD_DIRECTORY = "uploads"

def get_poppler_path():
    pdftoppm = shutil.which("pdftoppm")

    if pdftoppm:
        return os.path.dirname(pdftoppm)

    for path in ["/opt/homebrew/bin", "/usr/local/bin"]:
        if os.path.exists(os.path.join(path, "pdftoppm")):
            return path
    return None

def get_tesseract_path():
    tesseract = shutil.which("tesseract")

    if tesseract:
        return tesseract
    
    for path in ["/opt/homebrew/bin/tesseract", "/usr/local/bin/tesseract", "/usr/bin/tesseract"]:
        if os.path.exists(path):
            return path

    return "tesseract"

POPPLER_PATH = get_poppler_path()
TESSERACT_PATH = get_tesseract_path()