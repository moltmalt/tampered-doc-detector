from data_layer.file_repository import get_file
from data_layer.os_funcs import get_actual_filename

def file_format_checker(filename):
    image_extensions = ["png", "jpg"]
    document_extensions = ["pdf"]

    file_extension = (filename.split("."))[-1]

    if file_extension in image_extensions:
        if file_extension == "png":
            return "png"
        elif file_extension == "jpg":
            return "jpg"
    
    if file_extension in document_extensions:
        return "pdf"

def filename_repetition_checker(file_path):
    message = get_file(file_path)
    
    return message["status"]
    
def new_filename_maker(filename):
    file_format = file_format_checker(filename)

    old_filename = filename
    filename_no_extension = get_actual_filename(filename)
    new_filename = filename_no_extension + " 1" + "." + file_format

    return new_filename
    
def clean_json_response(json_response):
    return json_response.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
