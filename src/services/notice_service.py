import uuid
from datetime import datetime
from src.database import db
from src.models import Notice

def get_all_notices():
    records = Notice.query.order_by(Notice.date_posted.desc()).all()
    return [r.to_dict() for r in records]

def get_notices_for_user(role, user_name):
    all_notices = Notice.query.order_by(Notice.date_posted.desc()).all()
    filtered = []
    for n in all_notices:
        targets = n.target_roles or ['admin', 'professor', 'student']
        if role in targets or n.posted_by == user_name:
            filtered.append(n.to_dict())
    return filtered

def add_notice(title, content, posted_by, target_roles):
    new_notice = Notice(
        notice_id=str(uuid.uuid4()),
        title=title,
        content=content,
        date_posted=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        posted_by=posted_by,
        target_roles=target_roles
    )
    db.session.add(new_notice)
    db.session.commit()
    return new_notice.to_dict()

def delete_notice(notice_id):
    notice = db.session.get(Notice, notice_id)
    if notice:
        db.session.delete(notice)
        db.session.commit()
        return True
    return False
