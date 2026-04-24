import uuid
from src.utils.file_handler import read_json_file, write_json_file
from src.models import Attendance
from datetime import datetime

ATTENDANCE_FILE = 'attendance.json'

def get_all_attendance():
    return read_json_file(ATTENDANCE_FILE)

def get_attendance_by_date(date_str):
    records = get_all_attendance()
    return [r for r in records if r['date'] == date_str]

def get_attendance_for_student(student_id):
    records = get_all_attendance()
    return [r for r in records if r['student_id'] == student_id]

def record_attendance(student_id, date_str, status):
    records = get_all_attendance()
    # Check if a record already exists for this student on this date
    existing_record = next((r for r in records if r['student_id'] == student_id and r['date'] == date_str), None)
    
    if existing_record:
        existing_record['status'] = status
    else:
        new_attendance = Attendance(
            attendance_id=str(uuid.uuid4()),
            student_id=student_id,
            date=date_str,
            status=status
        )
        records.append(new_attendance.to_dict())
        
    write_json_file(ATTENDANCE_FILE, records)
    return True

def delete_attendance_for_students(student_ids):
    records = get_all_attendance()
    updated_records = [r for r in records if r['student_id'] not in student_ids]
    if len(records) != len(updated_records):
        write_json_file(ATTENDANCE_FILE, updated_records)
    return True
