import uuid
from src.database import db
from src.models import Student
from src.services.grade_service import delete_grades_for_students
from src.services.attendance_service import delete_attendance_for_students

def get_all_students():
    students = Student.query.all()
    return [s.to_dict() for s in students]

def add_student(name, age, email, enrollment_date):
    student = Student(
        student_id=str(uuid.uuid4()),
        name=name,
        age=age,
        email=email,
        enrollment_date=enrollment_date,
        enrolled_subjects=[]
    )
    db.session.add(student)
    db.session.commit()
    return student.to_dict()

def update_student(student_id, name, age, email):
    student = db.session.get(Student, student_id)
    if student:
        student.name = name
        student.age = age
        student.email = email
        db.session.commit()
        return student.to_dict()
    return None

def enroll_student_in_subject(student_id, subject_name):
    student = db.session.get(Student, student_id)
    if student:
        subjects = list(student.enrolled_subjects or [])
        if subject_name not in subjects:
            subjects.append(subject_name)
            student.enrolled_subjects = subjects
            db.session.commit()
        return student.to_dict()
    return None

def delete_student(student_id):
    student = db.session.get(Student, student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        delete_grades_for_students([student_id])
        delete_attendance_for_students([student_id])
        return True
    return False

def delete_multiple_students(student_ids):
    count = Student.query.filter(Student.student_id.in_(student_ids)).delete(synchronize_session=False)
    if count > 0:
        db.session.commit()
        delete_grades_for_students(student_ids)
        delete_attendance_for_students(student_ids)
        return True
    return False

def cleanup_orphaned_records():
    from src.models import Grade, Attendance
    
    valid_student_ids = db.session.query(Student.student_id).scalar_subquery()
    
    deleted_grades = Grade.query.filter(~Grade.student_id.in_(valid_student_ids)).delete(synchronize_session=False)
    deleted_attendance = Attendance.query.filter(~Attendance.student_id.in_(valid_student_ids)).delete(synchronize_session=False)
    
    db.session.commit()
    
    return {"deleted_grades": deleted_grades, "deleted_attendance": deleted_attendance}
