import uuid
from datetime import datetime
from src.database import db
from src.models import LibraryRecord

def get_all_library_records():
    records = LibraryRecord.query.all()
    return [r.to_dict() for r in records]

def add_library_record(student_id, book_title):
    new_record = LibraryRecord(
        record_id=str(uuid.uuid4()),
        student_id=student_id,
        book_title=book_title,
        checkout_date=datetime.now().strftime("%Y-%m-%d"),
        status="Borrowed"
    )
    db.session.add(new_record)
    db.session.commit()
    return new_record.to_dict()

def update_library_status(record_id, status):
    record = db.session.get(LibraryRecord, record_id)
    if record:
        record.status = status
        db.session.commit()
        return record.to_dict()
    return None

def delete_library_record(record_id):
    record = db.session.get(LibraryRecord, record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return True
    return False

def get_library_records_for_student(student_id):
    records = LibraryRecord.query.filter_by(student_id=student_id).all()
    return [r.to_dict() for r in records]
