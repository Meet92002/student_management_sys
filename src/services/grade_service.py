import uuid
from src.database import db
from src.models import Grade

def get_all_grades():
    grades = Grade.query.all()
    return [g.to_dict() for g in grades]

def get_grades_for_student(student_id):
    grades = Grade.query.filter_by(student_id=student_id).all()
    return [g.to_dict() for g in grades]

def add_grade(student_id, subject, score):
    new_grade = Grade(
        grade_id=str(uuid.uuid4()),
        student_id=student_id,
        subject=subject,
        score=float(score)
    )
    db.session.add(new_grade)
    db.session.commit()
    return True

def delete_grades_for_students(student_ids):
    Grade.query.filter(Grade.student_id.in_(student_ids)).delete(synchronize_session=False)
    db.session.commit()
    return True
