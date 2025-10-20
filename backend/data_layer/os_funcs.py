import os

def path_joiner(path_1, path_2, path_3 = None):
    combined_path = os.path.join(path_1, path_2)
    if path_3 is None:
        return combined_path
    
    final_path = os.path.join(combined_path, path_3)

    return final_path

def get_actual_file_name(filename):
    return os.path.splitext(filename)

