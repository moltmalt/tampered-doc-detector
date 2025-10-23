from .pdf_file_service import get_embedded_pdf_text, convert_pdf_to_image
from .img_file_service import ocr_img
from data_layer.os_funcs import get_filename_from_path

from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_embeddings_and_ocr(file_path):
    images = convert_pdf_to_image(file_path)
    embedded_texts = get_embedded_pdf_text(file_path)

    ocr_texts = ocr_img(images)
    
    sequence_similarity_score = SequenceMatcher(None, embedded_texts, ocr_texts).ratio()

    vector = vectorize_text(embedded_texts, ocr_texts)
    cosine_similarity_score = get_cosine_similarity(vector)

    return{
        "detection_technique":"embedding-ocr evaluation",
        "file_info":{
            "filename": get_filename_from_path(file_path),
            "file_path": file_path,
        },
        "analysis":{
            "sequence_similarity_score": round(sequence_similarity_score, 3), 
            "is_sequentially_tampered": bool(sequence_similarity_score < 0.95),
            "cosine_similarity_score": round(cosine_similarity_score, 3), 
            "is_semantically_tampered": bool(cosine_similarity_score < 0.8)
        }
    }

def vectorize_text(text_1, text_2=None):
    vector = TfidfVectorizer().fit_transform([text_1, text_2])

    return vector

def get_cosine_similarity(vector):
    cosine_similarity_score = cosine_similarity(vector[0:1], vector[1:2])[0][0]
    return float(cosine_similarity_score)
