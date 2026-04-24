import uuid
from datetime import datetime
from src.utils.file_handler import read_json_file, write_json_file

ASSIGNMENTS_FILE = 'assignments.json'
SUBMISSIONS_FILE = 'submissions.json'

def get_all_assignments():
    return read_json_file(ASSIGNMENTS_FILE)

def add_assignment(subject, title, description, deadline, prof_id):
    assignments = get_all_assignments()
    new_assignment = {
        "id": str(uuid.uuid4()),
        "prof_id": prof_id,
        "subject": subject,
        "title": title,
        "description": description,
        "deadline": deadline,
        "created_at": datetime.now().isoformat()
    }
    assignments.append(new_assignment)
    write_json_file(ASSIGNMENTS_FILE, assignments)
    return new_assignment

def get_all_submissions():
    return read_json_file(SUBMISSIONS_FILE)

def add_submission(assignment_id, student_id, content):
    submissions = get_all_submissions()
    
    # Check if student already submitted
    for sub in submissions:
        if sub['assignment_id'] == assignment_id and sub['student_id'] == student_id:
            sub['content'] = content
            sub['submitted_at'] = datetime.now().isoformat()
            write_json_file(SUBMISSIONS_FILE, submissions)
            return sub
            
    new_sub = {
        "id": str(uuid.uuid4()),
        "assignment_id": assignment_id,
        "student_id": student_id,
        "content": content,
        "submitted_at": datetime.now().isoformat(),
        "status": "Submitted"  # Changed by professor later to 'Graded'
    }
    submissions.append(new_sub)
    write_json_file(SUBMISSIONS_FILE, submissions)
    return new_sub

def grade_submission(submission_id, status, score=None):
    submissions = get_all_submissions()
    updated = None
    for sub in submissions:
        if sub['id'] == submission_id:
            sub['status'] = status
            if score is not None:
                sub['score'] = score
            updated = sub
            break
    if updated:
        write_json_file(SUBMISSIONS_FILE, submissions)
    return updated
