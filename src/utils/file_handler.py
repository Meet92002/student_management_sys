import os
import json

def get_data_path(filename):
    """Returns the absolute path to a file within the 'data' directory."""
    # current file is utils/file_handler.py
    # src/utils -> src -> student_management_sys
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, filename)

def read_json_file(filename):
    """Reads JSON data from a regular file."""
    filepath = get_data_path(filename)
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def write_json_file(filename, data):
    """Writes JSON data back to file."""
    filepath = get_data_path(filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
