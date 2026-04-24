import uuid
from src.utils.file_handler import read_json_file, write_json_file
from src.models import Student
from src.services.grade_service import delete_grades_for_students
from src.services.attendance_service import delete_attendance_for_students

STUDENTS_FILE = 'students.json'

def get_all_students():
    return read_json_file(STUDENTS_FILE)

def add_student(name, age, email, enrollment_date):
    students = get_all_students()
    student = Student(
        student_id=str(uuid.uuid4()),
        name=name,
        age=age,
        email=email,
        enrollment_date=enrollment_date
    )
    students.append(student.to_dict())
    write_json_file(STUDENTS_FILE, students)
    return student.to_dict()

def update_student(student_id, name, age, email):
    students = get_all_students()
    updated_student = None
    for student in students:
        if student['student_id'] == student_id:
            student['name'] = name
            student['age'] = age
            student['email'] = email
            updated_student = student
            break
    
    if updated_student:
        write_json_file(STUDENTS_FILE, students)
    return updated_student

def enroll_student_in_subject(student_id, subject_name):
    students = get_all_students()
    updated_student = None
    for student in students:
        if student['student_id'] == student_id:
            # Ensure the list exists for legacy records
            if 'enrolled_subjects' not in student:
                student['enrolled_subjects'] = []
            if subject_name not in student['enrolled_subjects']:
                student['enrolled_subjects'].append(subject_name)
            updated_student = student
            break
            
    if updated_student:
        write_json_file(STUDENTS_FILE, students)
    return updated_student

def delete_student(student_id):
    students = get_all_students()
    updated_students = [s for s in students if s['student_id'] != student_id]
    write_json_file(STUDENTS_FILE, updated_students)
    if len(students) != len(updated_students):
        delete_grades_for_students([student_id])
        delete_attendance_for_students([student_id])
        return True
    return False

def delete_multiple_students(student_ids):
    students = get_all_students()
    updated_students = [s for s in students if s['student_id'] not in student_ids]
    write_json_file(STUDENTS_FILE, updated_students)
    if len(students) != len(updated_students):
        delete_grades_for_students(student_ids)
        delete_attendance_for_students(student_ids)
        return True
    return False

def cleanup_orphaned_records():
    from src.services.grade_service import get_all_grades, write_json_file as write_grades, GRADES_FILE
    from src.services.attendance_service import get_all_attendance, write_json_file as write_attendance, ATTENDANCE_FILE
    
    valid_student_ids = {s['student_id'] for s in get_all_students()}
    
    grades = get_all_grades()
    valid_grades = [g for g in grades if g['student_id'] in valid_student_ids]
    write_grades(GRADES_FILE, valid_grades)
    
    attendance = get_all_attendance()
    valid_attendance = [a for a in attendance if a['student_id'] in valid_student_ids]
    write_attendance(ATTENDANCE_FILE, valid_attendance)
    
    return {"deleted_grades": len(grades) - len(valid_grades), "deleted_attendance": len(attendance) - len(valid_attendance)}
