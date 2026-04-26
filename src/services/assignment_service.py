import uuid
from datetime import datetime
from src.database import db
from src.models import Assignment, Submission

def get_all_assignments(prof_id=None):
    query = Assignment.query
    if prof_id:
        query = query.filter_by(prof_id=prof_id)
    records = query.all()
    return [r.to_dict() for r in records]

def add_assignment(subject, title, description, deadline, prof_id):
    new_assignment = Assignment(
        id=str(uuid.uuid4()),
        prof_id=prof_id,
        subject=subject,
        title=title,
        description=description,
        deadline=deadline,
        created_at=datetime.now().isoformat()
    )
    db.session.add(new_assignment)
    db.session.commit()
    return new_assignment.to_dict()

def get_all_submissions(assignment_ids=None):
    query = Submission.query
    if assignment_ids is not None:
        query = query.filter(Submission.assignment_id.in_(assignment_ids))
    records = query.all()
    return [r.to_dict() for r in records]

def add_submission(assignment_id, student_id, content):
    # Check if student already submitted
    existing = Submission.query.filter_by(assignment_id=assignment_id, student_id=student_id).first()
    
    if existing:
        existing.content = content
        existing.submitted_at = datetime.now().isoformat()
        db.session.commit()
        return existing.to_dict()
            
    new_sub = Submission(
        id=str(uuid.uuid4()),
        assignment_id=assignment_id,
        student_id=student_id,
        content=content,
        submitted_at=datetime.now().isoformat(),
        status="Submitted"
    )
    db.session.add(new_sub)
    db.session.commit()
    return new_sub.to_dict()

def grade_submission(submission_id, status, score=None):
    sub = db.session.get(Submission, submission_id)
    if sub:
        sub.status = status
        if score is not None:
            sub.score = float(score)
        db.session.commit()
        return sub.to_dict()
    return None
