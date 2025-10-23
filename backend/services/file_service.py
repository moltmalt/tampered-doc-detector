from core.config import UPLOAD_DIRECTORY 

from .business_logic import file_format_checker, filename_repetition_checker, new_filename_maker
from data_layer.file_repository import save_file_to_storage, get_file
from data_layer.os_funcs import path_joiner

async def save_file(file):
    content = await file.read()
    file_format = file_format_checker(file.filename)
    file_path = path_joiner(UPLOAD_DIRECTORY, file_format, file.filename)
    file_exists = filename_repetition_checker(file_path)

    if file_exists is True:
        new_filename = new_filename_maker(file.filename)
        new_file_path = path_joiner(UPLOAD_DIRECTORY, file_format, new_filename)
        return await save_file_to_storage(new_file_path, content)
    
    return await save_file_to_storage(file_path, content)


def rename_file_path(new_filename):
    folder_path = path_joiner(UPLOAD_DIRECTORY, file_format)
    new_filename_path = path_joiner(folder_path, new_filename)

    return new_filename_path

