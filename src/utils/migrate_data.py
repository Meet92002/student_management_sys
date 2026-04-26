import os
import sys
import json
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.app import app
from src.database import db
from src.models import User, Student, Grade, Attendance, Notice, Staff, Subject, LibraryRecord, Assignment, Submission
from src.utils.file_handler import get_data_path

def migrate():
    with app.app_context():
        # Helper to read JSON
        def load_json(filename):
            path = get_data_path(filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []

        # Helper to get or create ID
        def get_id(data, possible_keys):
            for k in possible_keys:
                if k in data:
                    return data[k]
            return str(uuid.uuid4())

        # Helper to filter data for model
        def filter_model_data(model, data):
            columns = [c.name for c in model.__table__.columns]
            return {k: v for k, v in data.items() if k in columns}

        print("Starting migration...")
        
        # Clear notices to ensure correct date mapping on re-run
        db.session.query(Notice).delete()
        users_data = load_json('users.json')
        for u in users_data:
            u_id = get_id(u, ['id', 'user_id'])
            if not db.session.get(User, u_id):
                filtered = filter_model_data(User, u)
                filtered['id'] = u_id
                db.session.add(User(**filtered))
        print(f"Migrated {len(users_data)} users.")

        # Students
        students_data = load_json('students.json')
        for s in students_data:
            s_id = get_id(s, ['student_id', 'id'])
            if not db.session.get(Student, s_id):
                filtered = filter_model_data(Student, s)
                filtered['student_id'] = s_id
                if 'enrolled_subjects' not in filtered:
                    filtered['enrolled_subjects'] = []
                db.session.add(Student(**filtered))
        print(f"Migrated {len(students_data)} students.")

        # Grades
        grades_data = load_json('grades.json')
        for g in grades_data:
            g_id = get_id(g, ['grade_id', 'id'])
            if not db.session.get(Grade, g_id):
                filtered = filter_model_data(Grade, g)
                filtered['grade_id'] = g_id
                db.session.add(Grade(**filtered))
        print(f"Migrated {len(grades_data)} grades.")

        # Attendance
        attendance_data = load_json('attendance.json')
        for a in attendance_data:
            a_id = get_id(a, ['attendance_id', 'id'])
            if not db.session.get(Attendance, a_id):
                filtered = filter_model_data(Attendance, a)
                filtered['attendance_id'] = a_id
                db.session.add(Attendance(**filtered))
        print(f"Migrated {len(attendance_data)} attendance records.")

        # Notices
        notices_data = load_json('notices.json')
        for n in notices_data:
            n_id = get_id(n, ['notice_id', 'id'])
            if not db.session.get(Notice, n_id):
                filtered = filter_model_data(Notice, n)
                filtered['notice_id'] = n_id
                # Map created_at to date_posted if missing
                if not filtered.get('date_posted'):
                    c_at = n.get('created_at') or n.get('date_posted')
                    if c_at:
                        if 'T' in c_at:
                            filtered['date_posted'] = c_at.replace('T', ' ').split('.')[0]
                        else:
                            filtered['date_posted'] = c_at
                db.session.add(Notice(**filtered))
        print(f"Migrated {len(notices_data)} notices.")

        # Staff
        staff_data = load_json('staff.json')
        for s in staff_data:
            s_id = get_id(s, ['staff_id', 'id'])
            if not db.session.get(Staff, s_id):
                filtered = filter_model_data(Staff, s)
                filtered['staff_id'] = s_id
                db.session.add(Staff(**filtered))
        print(f"Migrated {len(staff_data)} staff records.")

        # Subjects
        subjects_data = load_json('subjects.json')
        for s in subjects_data:
            s_id = get_id(s, ['subject_id', 'id'])
            if not db.session.get(Subject, s_id):
                filtered = filter_model_data(Subject, s)
                filtered['subject_id'] = s_id
                db.session.add(Subject(**filtered))
        print(f"Migrated {len(subjects_data)} subjects.")

        # Library
        library_data = load_json('library.json')
        for l in library_data:
            l_id = get_id(l, ['record_id', 'id'])
            if not db.session.get(LibraryRecord, l_id):
                filtered = filter_model_data(LibraryRecord, l)
                filtered['record_id'] = l_id
                db.session.add(LibraryRecord(**filtered))
        print(f"Migrated {len(library_data)} library records.")

        # Assignments
        assignments_data = load_json('assignments.json')
        for a in assignments_data:
            a_id = get_id(a, ['id', 'assignment_id'])
            if not db.session.get(Assignment, a_id):
                filtered = filter_model_data(Assignment, a)
                filtered['id'] = a_id
                db.session.add(Assignment(**filtered))
        print(f"Migrated {len(assignments_data)} assignments.")

        # Submissions
        submissions_data = load_json('submissions.json')
        for s in submissions_data:
            s_id = get_id(s, ['id', 'submission_id'])
            if not db.session.get(Submission, s_id):
                filtered = filter_model_data(Submission, s)
                filtered['id'] = s_id
                db.session.add(Submission(**filtered))
        print(f"Migrated {len(submissions_data)} submissions.")

        db.session.commit()
        print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()
