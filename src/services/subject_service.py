import uuid
from src.utils.file_handler import read_json_file, write_json_file
from src.models import Subject

SUBJECTS_FILE = 'subjects.json'

def get_all_subjects():
    return read_json_file(SUBJECTS_FILE)

def add_subject(name, description):
    records = get_all_subjects()
    new_subject = Subject(
        subject_id=str(uuid.uuid4()),
        name=name,
        description=description
    )
    records.append(new_subject.to_dict())
    write_json_file(SUBJECTS_FILE, records)
    return new_subject.to_dict()

def delete_subject(subject_id):
    records = get_all_subjects()
    updated = [r for r in records if r['subject_id'] != subject_id]
    write_json_file(SUBJECTS_FILE, updated)
    return len(records) != len(updated)
