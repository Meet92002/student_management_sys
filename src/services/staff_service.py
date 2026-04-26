import uuid
from src.database import db
from src.models import Staff

def get_all_staff():
    staff = Staff.query.all()
    return [s.to_dict() for s in staff]

def add_staff(name, role, department, email=None):
    new_staff = Staff(
        staff_id=str(uuid.uuid4()),
        name=name,
        role=role,
        department=department,
        email=email
    )
    db.session.add(new_staff)
    db.session.commit()
    return new_staff.to_dict()

def delete_staff(staff_id):
    staff = db.session.get(Staff, staff_id)
    if staff:
        db.session.delete(staff)
        db.session.commit()
        return True
    return False
