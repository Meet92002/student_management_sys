import os
import sys

# Add the parent directory to sys.path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from src.services.student_service import get_all_students, add_student, delete_student, update_student, delete_multiple_students, cleanup_orphaned_records, enroll_student_in_subject
from src.services.api_service import fetch_and_import_dummy_students
from src.services.reporting_service import get_subject_performance, get_student_attendance_summary
from src.services.attendance_service import get_attendance_by_date, record_attendance, get_attendance_for_student
from src.services.grade_service import get_grades_for_student, add_grade

from src.services.notice_service import get_all_notices, add_notice, delete_notice, get_notices_for_user
from src.services.staff_service import get_all_staff, add_staff, delete_staff
from src.services.subject_service import get_all_subjects, add_subject, delete_subject
from src.services.library_service import get_all_library_records, add_library_record, update_library_status, delete_library_record, get_library_records_for_student
from src.services.auth_service import init_admin_user, get_user_by_id, get_user_by_email
from src.services.assignment_service import get_all_assignments, add_assignment, get_all_submissions, add_submission, grade_submission
from src.services.quiz_service import get_all_quizzes, get_quiz_by_id, add_quiz, submit_quiz_result, get_quiz_rankings, get_student_quiz_results

from src.database import db
from src.models import User, Student, Grade, Attendance, Notice, Staff, Subject, LibraryRecord, Assignment, Submission, Quiz, QuizResult

app = Flask(__name__)
app.secret_key = 'elite_sms_super_secret_key_session'

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# DB Config
database_uri = os.environ.get('DATABASE_URI')

# If running on Render, ignore localhost strings that might be left over from .env
if os.environ.get('RENDER') == 'true' and database_uri and 'localhost' in database_uri:
    database_uri = None

if not database_uri:
    # Fallback to absolute path for SQLite
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_uri = 'sqlite:///' + os.path.join(project_root, 'student_management.db')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Init Auth Seed (Will be handled by migration or first run check)
with app.app_context():
    init_admin_user()

@app.route('/api/search')
@login_required
def global_search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    results = []
    
    # Search Students
    students = Student.query.filter(Student.name.ilike(f'%{query}%')).limit(5).all()
    for s in students:
        results.append({"type": "Student", "name": s.name, "url": url_for('student_profile', student_id=s.student_id)})
        
    # Search Staff
    staff = Staff.query.filter(Staff.name.ilike(f'%{query}%')).limit(5).all()
    for st in staff:
        results.append({"type": "Staff", "name": st.name, "url": "#"})
        
    # Search Subjects
    subjects = Subject.query.filter(Subject.name.ilike(f'%{query}%')).limit(5).all()
    for subj in subjects:
        results.append({"type": "Subject", "name": subj.name, "url": url_for('subjects_page')})
        
    return jsonify(results)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# Role Decorators
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def professor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'professor']:
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = get_user_by_email(email)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('signup.html')
            
        if get_user_by_email(email):
            flash('Email address already exists', 'danger')
            return render_template('signup.html')
            
        import uuid
        user_id = f"u{uuid.uuid4().hex[:8]}"
        
        from src.services.auth_service import create_user
        new_user = create_user(user_id, name, email, password, role)
        
        if new_user:
            # Also create the corresponding profile
            if role == 'student':
                from src.models import Student
                import datetime
                s = Student(student_id=user_id, name=name, email=email, age=18, enrollment_date=datetime.date.today().isoformat(), enrolled_subjects=[])
                db.session.add(s)
                db.session.commit()
            elif role == 'professor':
                from src.models import Staff
                staff = Staff(staff_id=user_id, name=name, email=email, role='Professor', department='General')
                db.session.add(staff)
                db.session.commit()
                
            login_user(new_user)
            flash('Account created successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Error creating account', 'danger')
            
    return render_template('signup.html')

@app.route('/docs')
def docs_page():
    return render_template('docs.html')

@app.route('/api/docs/content')
def docs_content():
    import os
    docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Elite_SMS_Project_Documentation.md')
    try:
        with open(docs_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return str(e)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    """Route user to correct dashboard"""
    if current_user.role == 'admin':
        return render_template('dashboard.html') # Admin Dashboard
    elif current_user.role == 'professor':
        # Map user to staff UUID via email
        staff_list = get_all_staff()
        me = next((s for s in staff_list if s.get('email') == current_user.email), None)
        my_uuid = me['staff_id'] if me else current_user.id

        my_assignments = get_all_assignments(prof_id=my_uuid)
        my_assign_ids = [a['id'] for a in my_assignments]
        
        # Unique Subjects I teach
        class_count = len({a['subject'] for a in my_assignments})
        
        # Get submissions only for MY assignments
        submissions = get_all_submissions(assignment_ids=my_assign_ids) if my_assign_ids else []
        students = get_all_students()
        
        # Pending Submissions for MY assignments
        pending_list = []
        for s in submissions:
            if s['status'] == 'Submitted':
                student = next((std for std in students if std['student_id'] == s['student_id']), None)
                assignment = next((a for a in my_assignments if a['id'] == s['assignment_id']), None)
                pending_list.append({
                    'student_name': student['name'] if student else 'Unknown',
                    'assignment_title': assignment['title'] if assignment else 'Unknown',
                    'subject': assignment['subject'] if assignment else 'Unknown',
                    'submitted_at': s['submitted_at'][:10] if s.get('submitted_at') else 'N/A'
                })
        
        pending_count = len(pending_list)

        # Attendance Summary for Table
        att_summary = get_student_attendance_summary()

        return render_template('professor_dashboard.html', 
                               class_count=class_count, 
                               pending_count=pending_count,
                               pending_list=pending_list,
                               att_summary=att_summary)
    elif current_user.role == 'student':
        students = get_all_students()
        # Find student record by email since current_user.id is 'uX' but students.json uses UUIDs
        me = next((s for s in students if s['email'] == current_user.email), None)
        
        if not me:
            return render_template('student_dashboard.html', 
                                   enrolled_count=0, att_rate=0, due_count=0,
                                   graph_labels=[], graph_values=[], 
                                   att_labels=[], att_values=[])
            
        my_uuid = me['student_id']
        enrolled_count = len(me['enrolled_subjects']) if 'enrolled_subjects' in me else 0
        
        att = get_attendance_for_student(my_uuid)
        total_days = len(att)
        present_days = sum(1 for a in att if a['status'] == 'Present')
        absent_days = total_days - present_days
        att_rate = int((present_days / total_days) * 100) if total_days > 0 else 100
        
        assignments = get_all_assignments()
        submissions = get_all_submissions()
        sub_ids = {s['assignment_id'] for s in submissions if s['student_id'] == my_uuid}
        due_count = sum(1 for a in assignments if a['id'] not in sub_ids)

        # Graph Data: Performance by Subject
        my_grades = get_grades_for_student(my_uuid)
        perf_data = {}
        for g in my_grades:
            subj = g['subject']
            if subj not in perf_data:
                perf_data[subj] = []
            perf_data[subj].append(g['score'])
        
        graph_labels = list(perf_data.keys())
        graph_values = [sum(scores)/len(scores) for scores in perf_data.values()]

        # Latest Attendance Records (Reverse for descending order)
        att.sort(key=lambda x: x['date'], reverse=True)
        last_10 = att[:10]
        att_labels = [a['date'] for a in last_10]
        att_values = [1 if a['status'] == 'Present' else 0 for a in last_10]

        return render_template('student_dashboard.html',
                               enrolled_count=enrolled_count,
                               att_rate=att_rate,
                               total_days=total_days,
                               present_days=present_days,
                               absent_days=absent_days,
                               due_count=due_count,
                               graph_labels=graph_labels,
                               graph_values=graph_values,
                               att_labels=att_labels,
                               att_values=att_values,
                               student_id=my_uuid)

@app.route('/records')
@login_required
def records():
    if current_user.role not in ['admin', 'professor']:
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))
    return render_template('records.html')

@app.route('/api/students', methods=['GET', 'POST'])
@login_required
def students_api():
    if request.method == 'GET':
        search = request.args.get('search', '').lower()
        students = get_all_students()
        
        if search:
            # Global search across all records
            students = [s for s in students if search in s['name'].lower() or search in s['email'].lower()]
        
        # Pagination support
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)
        
        # We need to reverse it so newest is first just like before
        students.reverse()
        
        start = (page - 1) * limit
        end = start + limit
        paginated_students = students[start:end]
        
        return jsonify({
            "data": paginated_students,
            "total": len(students),
            "page": page,
            "limit": limit
        })
    elif request.method == 'POST':
        data = request.json
        student = add_student(data['name'], data['age'], data['email'], data['enrollment_date'])
        return jsonify(student), 201

@app.route('/api/students/me')
@login_required
def get_my_student_profile():
    # Use direct query instead of filtering all students
    student = Student.query.filter_by(email=current_user.email).first()
    if student:
        return jsonify(student.to_dict())
    return jsonify({"error": "Profile not found"}), 404

@app.route('/api/students/<student_id>', methods=['GET'])
@login_required
def get_student_by_id_api(student_id):
    # Use direct database lookup
    student = db.session.get(Student, student_id)
    if student:
        return jsonify(student.to_dict())
    return jsonify({"error": "Student not found"}), 404

@app.route('/api/students/<student_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_student_api(student_id):
    success = delete_student(student_id)
    return jsonify({"success": success})

@app.route('/api/students/bulk-delete', methods=['POST'])
@login_required
@admin_required
def bulk_delete_students_api():
    data = request.json
    student_ids = data.get('student_ids', [])
    if not student_ids:
        return jsonify({"error": "No student IDs provided"}), 400
    success = delete_multiple_students(student_ids)
    return jsonify({"success": success})

@app.route('/api/students/<student_id>', methods=['PUT'])
@login_required
@admin_required
def update_student_api(student_id):
    data = request.json
    updated_student = update_student(student_id, data['name'], data['age'], data['email'])
    if updated_student:
        return jsonify(updated_student), 200
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route('/api/students/<student_id>/enroll', methods=['POST'])
def enroll_student_api(student_id):
    data = request.json
    subject = data.get('subject')
    if not subject:
        return jsonify({"error": "Subject required"}), 400
    updated = enroll_student_in_subject(student_id, subject)
    if updated:
        return jsonify(updated)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route('/api/import-dummy', methods=['POST'])
def import_dummy():
    count = fetch_and_import_dummy_students()
    return jsonify({"message": f"Imported {count} students"})

@app.route('/api/maintenance/cleanup', methods=['POST'])
def cleanup_orphaned_data():
    results = cleanup_orphaned_records()
    return jsonify({"success": True, "results": results})

@app.route('/api/reports/subjects', methods=['GET'])
def subject_reports():
    return jsonify(get_subject_performance())

@app.route('/api/reports/attendance', methods=['GET'])
def attendance_reports():
    return jsonify(get_student_attendance_summary())

@app.route('/api/export/csv', methods=['GET'])
def export_students_csv():
    students = get_all_students()
    df = pd.DataFrame(students)
    csv_data = df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=students_export.csv"}
    )

@app.route('/attendance')
@login_required
@professor_required
def attendance_page():
    return render_template('attendance.html')

@app.route('/api/attendance', methods=['GET', 'POST'])
@login_required
@professor_required
def attendance_api():
    if request.method == 'GET':
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({"error": "Date parameter is required"}), 400
        records = get_attendance_by_date(date_str)
        return jsonify(records)
    elif request.method == 'POST':
        data = request.json
        success = record_attendance(data['student_id'], data['date'], data['status'])
        return jsonify({"success": success})

@app.route('/api/attendance/student/<student_id>', methods=['GET'])
@login_required
def attendance_student_api(student_id):
    records = get_attendance_for_student(student_id)
    return jsonify(records)

@app.route('/grades')
@login_required
@professor_required
def grades_page():
    return render_template('grades.html')

@app.route('/api/grades', methods=['GET', 'POST'])
@login_required
def grades_api():
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        if not student_id:
            return jsonify({"error": "student_id parameter is required"}), 400
        
        # Security: Students can only view their own grades
        if current_user.role == 'student':
            me = Student.query.filter_by(email=current_user.email).first()
            if not me or me.student_id != student_id:
                return jsonify({"error": "Unauthorized to view these grades"}), 403

        records = get_grades_for_student(student_id)
        return jsonify(records)
    elif request.method == 'POST':
        # Only professors and admins can add grades
        if current_user.role not in ['admin', 'professor']:
            return jsonify({"error": "Unauthorized to add grades"}), 403
            
        data = request.json
        success = add_grade(data['student_id'], data['subject'], data['score'])
        return jsonify({"success": success})

@app.route('/student/<student_id>')
@login_required
def student_profile(student_id):
    return render_template('profile.html', student_id=student_id)

@app.route('/my-profile')
@login_required
def my_profile():
    if current_user.role == 'student':
        students = get_all_students()
        me = next((s for s in students if s['email'] == current_user.email), None)
        if me:
            return redirect(url_for('student_profile', student_id=me['student_id']))
    flash("Profile not found.", "danger")
    return redirect(url_for('dashboard'))

@app.route('/notices')
@login_required
def notices_page():
    return render_template('notices.html')

@app.route('/api/notices', methods=['GET', 'POST'])
@login_required
def notices_api():
    if request.method == 'GET':
        return jsonify(get_notices_for_user(current_user.role, current_user.name))
    elif request.method == 'POST':
        if current_user.role not in ['admin', 'professor']:
            return jsonify({"error": "Unauthorized"}), 403
        
        data = request.json
        title = data.get('title')
        content = data.get('content')
        
        target_roles = []
        if current_user.role == 'admin':
            # Use target_roles from request if provided, otherwise default to all
            target_roles = data.get('target_roles', ['admin', 'professor', 'student'])
        elif current_user.role == 'professor':
            # Professor sends Notice > Student must be shows, admin optional
            target_roles = ['student']
            if data.get('show_to_admin'):
                target_roles.append('admin')
        
        return jsonify(add_notice(title, content, current_user.name, target_roles))

@app.route('/api/notices/<notice_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_notice_api(notice_id):
    return jsonify({"success": delete_notice(notice_id)})

# Staff Directory
@app.route('/staff')
@login_required
@admin_required
def staff_page():
    return render_template('staff.html')

@app.route('/api/staff', methods=['GET', 'POST'])
def staff_api():
    if request.method == 'GET':
        return jsonify(get_all_staff())
    elif request.method == 'POST':
        data = request.json
        return jsonify(add_staff(data['name'], data['role'], data['department']))

@app.route('/api/staff/<staff_id>', methods=['DELETE'])
def delete_staff_api(staff_id):
    return jsonify({"success": delete_staff(staff_id)})

@app.route('/api/staff/count', methods=['GET'])
@login_required
def staff_count_api():
    staff = get_all_staff()
    # Filter for those with role 'Teacher' or 'Professor' (based on staff.json roles)
    professors = [s for s in staff if s['role'] in ['Teacher', 'Professor']]
    return jsonify({"total": len(professors)})

# Subjects
@app.route('/subjects')
@login_required
@professor_required
def subjects_page():
    return render_template('subjects.html')

@app.route('/api/subjects', methods=['GET', 'POST'])
@login_required
def subjects_api():
    if request.method == 'GET':
        all_subs = get_all_subjects()
        if current_user.role == 'professor':
            from src.services.staff_service import get_all_staff
            staff_list = get_all_staff()
            me = next((s for s in staff_list if s['email'] == current_user.email), None)
            if me:
                # Return subjects matching their department OR global subjects (no department)
                return jsonify([s for s in all_subs if s.get('department') == me['department']])
        return jsonify(all_subs)
    elif request.method == 'POST':
        data = request.json
        if current_user.role == 'admin':
            return jsonify(add_subject(data['name'], data['description'], data.get('department')))
        elif current_user.role == 'professor':
            from src.services.staff_service import get_all_staff
            staff_list = get_all_staff()
            me = next((s for s in staff_list if s['email'] == current_user.email), None)
            if me:
                # Professors automatically create subjects for THEIR department
                return jsonify(add_subject(data['name'], data['description'], me['department']))
            return jsonify({"error": "Professor record not found"}), 404
        return jsonify({"error": "Unauthorized"}), 403

@app.route('/api/subjects/<subject_id>', methods=['DELETE'])
@login_required
@professor_required
def delete_subject_api(subject_id):
    return jsonify({"success": delete_subject(subject_id)})

# Library Tracker
@app.route('/library')
@login_required
@admin_required
def library_page():
    return render_template('library.html')

@app.route('/api/library', methods=['GET', 'POST'])
def library_api():
    if request.method == 'GET':
        return jsonify(get_all_library_records())
    elif request.method == 'POST':
        data = request.json
        return jsonify(add_library_record(data['student_id'], data['book_title']))

@app.route('/api/library/<record_id>', methods=['PUT', 'DELETE'])
def manage_library_api(record_id):
    if request.method == 'PUT':
        data = request.json
        return jsonify(update_library_status(record_id, data['status']))
    elif request.method == 'DELETE':
        return jsonify({"success": delete_library_record(record_id)})

@app.route('/api/library/student/<student_id>', methods=['GET'])
@login_required
def library_student_api(student_id):
    """Get all library records for a specific student."""
    records = get_library_records_for_student(student_id)
    return jsonify(records)

@app.route('/assignments')
@login_required
def assignments_page():
    student_uuid = None
    if current_user.role == 'student':
        students = get_all_students()
        me = next((s for s in students if s['email'] == current_user.email), None)
        if me:
            student_uuid = me['student_id']
            
    return render_template('assignments.html', student_uuid=student_uuid)

@app.route('/api/assignments', methods=['GET', 'POST'])
@login_required
def assignments_api():
    # Helper to get professor ID
    from src.services.staff_service import get_all_staff
    staff_list = get_all_staff()
    me = next((s for s in staff_list if s['email'] == current_user.email), None)
    my_uuid = me['staff_id'] if me else current_user.id

    if request.method == 'GET':
        if current_user.role == 'professor':
            return jsonify(get_all_assignments(prof_id=my_uuid))
        return jsonify(get_all_assignments())
    elif request.method == 'POST':
        if current_user.role not in ['professor', 'admin']:
            return jsonify({"error": "Unauthorized"}), 403
        data = request.json
        
        if current_user.role == 'professor' and me:
            # Check if the chosen subject belongs to the professor's department
            all_subs = get_all_subjects()
            target_sub = next((s for s in all_subs if s['name'] == data['subject']), None)
            if target_sub and target_sub.get('department') != me['department']:
                return jsonify({"error": f"You can only create assignments for subjects in {me['department']}"}), 403
            elif not target_sub and data['subject'] != me['department']:
                # Fallback for legacy subjects or if subject name was used as department
                return jsonify({"error": f"You can only create assignments for {me['department']}"}), 403
        
        return jsonify(add_assignment(data['subject'], data['title'], data['description'], data['deadline'], my_uuid))

@app.route('/api/submissions', methods=['GET', 'POST', 'PUT'])
@login_required
def submissions_api():
    if request.method == 'GET':
        if current_user.role == 'professor':
            # Only show submissions for THIS professor's assignments
            from src.services.staff_service import get_all_staff
            staff_list = get_all_staff()
            me = next((s for s in staff_list if s['email'] == current_user.email), None)
            my_uuid = me['staff_id'] if me else current_user.id
            
            my_assignments = get_all_assignments(prof_id=my_uuid)
            my_assign_ids = [a['id'] for a in my_assignments]
            return jsonify(get_all_submissions(assignment_ids=my_assign_ids))
            
        return jsonify(get_all_submissions())
    elif request.method == 'POST':
        if current_user.role != 'student':
            return jsonify({"error": "Only students can submit."}), 403
        data = request.json
        # Map user to student UUID via email
        students = get_all_students()
        me = next((s for s in students if s['email'] == current_user.email), None)
        my_uuid = me['student_id'] if me else current_user.id
        
        return jsonify(add_submission(data['assignment_id'], my_uuid, data['content']))
    elif request.method == 'PUT':
        if current_user.role == 'student':
            return jsonify({"error": "Unauthorized"}), 403
        data = request.json
        score = data.get('score')
        submission_id = data.get('submission_id')
        
        updated = grade_submission(submission_id, data['status'], score)
        if updated and score is not None:
            # Also record in general grades for reporting
            # Need to find the subject from assignment
            assignments = get_all_assignments()
            target_assign = next((a for a in assignments if a['id'] == updated['assignment_id']), None)
            if target_assign:
                add_grade(updated['student_id'], target_assign['subject'], score)
                
        return jsonify(updated)

@app.route('/api/attendance/summary')
@login_required
def attendance_summary_api():
    """Get global attendance summary stats for admin/professor dashboard"""
    summary = get_student_attendance_summary()
    if not summary:
        return jsonify({"average_rate": 0, "total_records": 0, "students_counted": 0})
    
    avg_rate = int(sum(s['attendance_rate'] for s in summary) / len(summary))
    return jsonify({
        "average_rate": avg_rate,
        "students_counted": len(summary),
        "data": summary
    })
    
@app.route('/api/submissions/assignment/<assignment_id>', methods=['GET'])
@login_required
def assignment_submissions_api(assignment_id):
    """Get all submissions for a specific assignment (for professors)"""
    if current_user.role == 'student':
        return jsonify({"error": "Unauthorized"}), 403
    
    submissions = get_all_submissions()
    students = get_all_students()
    std_map = {s['student_id']: s['name'] for s in students}
    
    filtered = []
    for s in submissions:
        if s['assignment_id'] == assignment_id:
            s['student_name'] = std_map.get(s['student_id'], 'Unknown Student')
            filtered.append(s)
            
    return jsonify(filtered)

@app.route('/api/exam-report')
@login_required
def exam_report_api():
    student_uuid = None
    if current_user.role == 'student':
        students = get_all_students()
        me = next((s for s in students if s['email'] == current_user.email), None)
        student_uuid = me['student_id'] if me else current_user.id
    else:
        student_uuid = request.args.get('student_id')
        if not student_uuid:
            return jsonify({"error": "student_id required"}), 400

    from src.services.quiz_service import get_all_quizzes, get_student_quiz_results
    all_quizzes = get_all_quizzes()
    my_results = get_student_quiz_results(student_uuid)
    
    # Check if student completed all quizzes
    if len(my_results) < len(all_quizzes):
        return jsonify({
            "status": "Incomplete",
            "message": "You must complete all quizzes to see the final report.",
            "completed": len(my_results),
            "total": len(all_quizzes)
        })

    # Calculate total marks (5 per question)
    total_marks = sum([r['score'] * 5 for r in my_results])
    max_marks = sum([r['total_questions'] * 5 for r in my_results])

    # Calculate Rankings
    all_students = get_all_students()
    leaderboard = []
    for s in all_students:
        s_results = get_student_quiz_results(s['student_id'])
        if len(s_results) == len(all_quizzes):
            s_total = sum([r['score'] * 5 for r in s_results])
            leaderboard.append({
                "student_id": s['student_id'],
                "name": s['name'],
                "total_marks": s_total
            })
    
    leaderboard.sort(key=lambda x: x['total_marks'], reverse=True)
    
    my_rank = next((i + 1 for i, s in enumerate(leaderboard) if s['student_id'] == student_uuid), None)
    
    return jsonify({
        "status": "Complete",
        "total_marks": total_marks,
        "max_marks": max_marks,
        "rank": my_rank,
        "total_students": len(leaderboard),
        "leaderboard": leaderboard if current_user.role in ['admin', 'professor'] else None,
        "my_scores": [{"quiz": next((q['title'] for q in all_quizzes if q['id'] == r['quiz_id']), "Quiz"), "marks": r['score'] * 5} for r in my_results]
    })

@app.route('/quizzes')
@login_required
def quizzes_page():
    if current_user.role == 'professor':
        return render_template('professor_quizzes.html')
    return render_template('quizzes.html')

@app.route('/api/quizzes', methods=['GET', 'POST'])
@login_required
def quizzes_api():
    # Helper to get professor ID
    from src.services.staff_service import get_all_staff
    staff_list = get_all_staff()
    me = next((s for s in staff_list if s['email'] == current_user.email), None)
    my_uuid = me['staff_id'] if me else current_user.id

    if request.method == 'GET':
        quizzes = []
        if current_user.role == 'professor':
            quizzes = get_all_quizzes(prof_id=my_uuid)
        else:
            quizzes = get_all_quizzes()
            
        if current_user.role == 'student':
            # Map user to student UUID
            students = get_all_students()
            me = next((s for s in students if s['email'] == current_user.email), None)
            
            if not me:
                return jsonify([]) # No student profile, no quizzes
            
            my_uuid = me['student_id']
            enrolled_subjects = me.get('enrolled_subjects', [])
            
            # Filter quizzes by enrollment
            quizzes = [q for q in quizzes if q['subject'] in enrolled_subjects]
            
            # Get attempted quiz IDs
            results = get_student_quiz_results(my_uuid)
            attempted_ids = {r['quiz_id'] for r in results}
            
            for q in quizzes:
                q['attempted'] = q['id'] in attempted_ids
        return jsonify(quizzes)
    elif request.method == 'POST':
        data = request.json
        if current_user.role == 'professor':
            if me:
                # Check if the chosen subject belongs to the professor's department
                all_subs = get_all_subjects()
                target_sub = next((s for s in all_subs if s['name'] == data['subject']), None)
                if target_sub and target_sub.get('department') != me['department']:
                    return jsonify({"error": f"You can only create quizzes for subjects in {me['department']}"}), 403
                elif not target_sub and data['subject'] != me['department']:
                    # Fallback
                    return jsonify({"error": f"You can only create quizzes for {me['department']}"}), 403
            
            return jsonify(add_quiz(data['title'], data['subject'], my_uuid, data['questions']))
        
        return jsonify({"error": "Unauthorized"}), 403

@app.route('/api/quizzes/<quiz_id>', methods=['GET'])
@login_required
def get_quiz_api(quiz_id):
    quiz = get_quiz_by_id(quiz_id, shuffle=False) # Get initial to check subject
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404
        
    if current_user.role == 'student':
        students = get_all_students()
        me = next((s for s in students if s['email'] == current_user.email), None)
        if not me or quiz['subject'] not in me.get('enrolled_subjects', []):
            return jsonify({"error": "You are not enrolled in the subject for this quiz."}), 403

    # Shuffle for students, not for professors
    shuffle = (current_user.role == 'student')
    quiz = get_quiz_by_id(quiz_id, shuffle=shuffle)
    return jsonify(quiz)

@app.route('/api/quizzes/<quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz_api(quiz_id):
    if current_user.role != 'student':
        return jsonify({"error": "Only students can submit quizzes"}), 403
    
    quiz = get_quiz_by_id(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    # Map user to student UUID via email
    students = get_all_students()
    me = next((s for s in students if s['email'] == current_user.email), None)
    
    if not me or quiz['subject'] not in me.get('enrolled_subjects', []):
        return jsonify({"error": "You are not enrolled in the subject for this quiz."}), 403

    my_uuid = me['student_id']
    
    data = request.json
    result = submit_quiz_result(quiz_id, my_uuid, data['answers'])
    return jsonify(result)

@app.route('/api/quizzes/<quiz_id>/rankings', methods=['GET'])
@login_required
def quiz_rankings_api(quiz_id):
    rankings = get_quiz_rankings(quiz_id)
    # Map student IDs to names
    students = get_all_students()
    std_map = {s['student_id']: s['name'] for s in students}
    for r in rankings:
        r['student_name'] = std_map.get(r['student_id'], 'Unknown Student')
    return jsonify(rankings)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
