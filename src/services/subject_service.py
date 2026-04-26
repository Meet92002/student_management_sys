import uuid
from src.database import db
from src.models import Subject

def get_all_subjects():
    subjects = Subject.query.all()
    return [s.to_dict() for s in subjects]

def add_subject(name, description, department=None):
    new_subject = Subject(
        subject_id=str(uuid.uuid4()),
        name=name,
        description=description,
        department=department
    )
    db.session.add(new_subject)
    db.session.commit()
    return new_subject.to_dict()

def delete_subject(subject_id):
    subj = db.session.get(Subject, subject_id)
    if subj:
        db.session.delete(subj)
        db.session.commit()
        return True
    return False
