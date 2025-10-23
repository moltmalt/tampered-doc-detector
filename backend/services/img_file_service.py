from core.config import TESSERACT_PATH

import pytesseract

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def ocr_img(images):
    ocr_texts = ""

    for img in images:
        ocr_texts = ocr_texts + pytesseract.image_to_string(img)

    return ocr_texts