import uuid
from src.utils.file_handler import read_json_file, write_json_file
from src.models import Staff

STAFF_FILE = 'staff.json'

def get_all_staff():
    return read_json_file(STAFF_FILE)

def add_staff(name, role, department):
    records = get_all_staff()
    new_staff = Staff(
        staff_id=str(uuid.uuid4()),
        name=name,
        role=role,
        department=department
    )
    records.append(new_staff.to_dict())
    write_json_file(STAFF_FILE, records)
    return new_staff.to_dict()

def delete_staff(staff_id):
    records = get_all_staff()
    updated = [r for r in records if r['staff_id'] != staff_id]
    write_json_file(STAFF_FILE, updated)
    return len(records) != len(updated)
