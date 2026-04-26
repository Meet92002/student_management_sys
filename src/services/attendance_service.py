import uuid
from src.database import db
from src.models import Attendance

def get_all_attendance():
    records = Attendance.query.all()
    return [r.to_dict() for r in records]

def get_attendance_by_date(date_str):
    records = Attendance.query.filter_by(date=date_str).all()
    return [r.to_dict() for r in records]

def get_attendance_for_student(student_id):
    records = Attendance.query.filter_by(student_id=student_id).all()
    return [r.to_dict() for r in records]

def record_attendance(student_id, date_str, status):
    existing = Attendance.query.filter_by(student_id=student_id, date=date_str).first()
    if existing:
        existing.status = status
    else:
        new_attendance = Attendance(
            attendance_id=str(uuid.uuid4()),
            student_id=student_id,
            date=date_str,
            status=status
        )
        db.session.add(new_attendance)
    db.session.commit()
    return True

def delete_attendance_for_students(student_ids):
    Attendance.query.filter(Attendance.student_id.in_(student_ids)).delete(synchronize_session=False)
    db.session.commit()
    return True
