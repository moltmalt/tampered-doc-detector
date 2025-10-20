from data_layer.file_repository import get_file

def file_format_checker(file):
    image_extensions = ["png", "jpg"]
    document_extensions = ["pdf"]

    filename = file.filename
    file_extension = (filename.split("."))[-1]

    if file_extension in image_extensions:
        if file_extension == "png":
            return "png"
        elif file_extension == "jpg":
            return "jpg"
    
    if file_extension in document_extensions:
        return "pdf"

def file_name_repetition_checker(file_path):
    message = get_file(file_path)
    
    return message["status"]
    
def new_filename_maker(filename):
    file_format = file_format_checker(filename)

    old_filename = filename
    file_name_no_extension = get_actual_file_name(filename)
    new_filename = file_name_no_extension + " 1" + file_format

    return new_filename
    


