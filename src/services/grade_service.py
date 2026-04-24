import uuid
from src.utils.file_handler import read_json_file, write_json_file
from src.models import Grade

GRADES_FILE = 'grades.json'

def get_all_grades():
    return read_json_file(GRADES_FILE)

def get_grades_for_student(student_id):
    records = get_all_grades()
    return [r for r in records if r['student_id'] == student_id]

def add_grade(student_id, subject, score):
    records = get_all_grades()
    
    new_grade = Grade(
        grade_id=str(uuid.uuid4()),
        student_id=student_id,
        subject=subject,
        score=float(score)
    )
    records.append(new_grade.to_dict())
    
    write_json_file(GRADES_FILE, records)
    return True

def delete_grades_for_students(student_ids):
    records = get_all_grades()
    updated_records = [r for r in records if r['student_id'] not in student_ids]
    if len(records) != len(updated_records):
        write_json_file(GRADES_FILE, updated_records)
    return True
