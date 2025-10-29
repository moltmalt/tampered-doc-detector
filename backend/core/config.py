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

POPPLER_PATH = get_poppler_path()