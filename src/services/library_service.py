import uuid
from datetime import datetime
from src.utils.file_handler import read_json_file, write_json_file
from src.models import LibraryRecord

LIBRARY_FILE = 'library.json'

def get_all_library_records():
    return read_json_file(LIBRARY_FILE)

def add_library_record(student_id, book_title):
    records = get_all_library_records()
    new_record = LibraryRecord(
        record_id=str(uuid.uuid4()),
        student_id=student_id,
        book_title=book_title,
        checkout_date=datetime.now().strftime("%Y-%m-%d"),
        status="Borrowed"
    )
    records.append(new_record.to_dict())
    write_json_file(LIBRARY_FILE, records)
    return new_record.to_dict()

def update_library_status(record_id, status):
    records = get_all_library_records()
    updated = None
    for r in records:
        rid = r.get('record_id') or r.get('id')
        if rid == record_id:
            r['status'] = status
            updated = r
            break
    if updated:
        write_json_file(LIBRARY_FILE, records)
    return updated

def delete_library_record(record_id):
    records = get_all_library_records()
    updated = [r for r in records if (r.get('record_id') or r.get('id')) != record_id]
    write_json_file(LIBRARY_FILE, updated)
    return len(records) != len(updated)

def get_library_records_for_student(student_id):
    """Returns all library records associated with a specific student."""
    records = get_all_library_records()
    return [r for r in records if r['student_id'] == student_id]
