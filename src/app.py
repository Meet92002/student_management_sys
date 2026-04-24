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

app = Flask(__name__)
app.secret_key = 'elite_sms_super_secret_key_session'

# Init Auth Seed
init_admin_user()

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
        from src.services.staff_service import get_all_staff
        from src.services.student_service import get_all_students
        
        # Map user to staff UUID via email
        staff_list = get_all_staff()
        me = next((s for s in staff_list if s.get('email') == current_user.email), None)
        my_uuid = me['staff_id'] if me else current_user.id

        assignments = get_all_assignments()
        submissions = get_all_submissions()
        students = get_all_students()
        
        # Filter assignments created by THIS professor
        my_assignments = [a for a in assignments if a.get('prof_id') == my_uuid]
        my_assign_ids = {a['id'] for a in my_assignments}
        
        # Unique Subjects I teach
        class_count = len({a['subject'] for a in my_assignments})
        
        # Pending Submissions for MY assignments
        pending_list = []
        for s in submissions:
            if s['assignment_id'] in my_assign_ids and s['status'] == 'Submitted':
                student = next((std for std in students if std['student_id'] == s['student_id']), None)
                assignment = next((a for a in assignments if a['id'] == s['assignment_id']), None)
                pending_list.append({
                    'student_name': student['name'] if student else 'Unknown',
                    'assignment_title': assignment['title'] if assignment else 'Unknown',
                    'subject': assignment['subject'] if assignment else 'Unknown',
                    'submitted_at': s['submitted_at'][:10]
                })
        
        pending_count = len(pending_list)

        # Attendance Summary for Graph
        att_summary = get_student_attendance_summary()
        prof_att_labels = [s['name'] for s in att_summary]
        prof_att_values = [s['attendance_rate'] for s in att_summary]

        return render_template('professor_dashboard.html', 
                               class_count=class_count, 
                               pending_count=pending_count,
                               pending_list=pending_list,
                               prof_att_labels=prof_att_labels,
                               prof_att_values=prof_att_values)
    elif current_user.role == 'student':
        from src.services.student_service import get_all_students
        from src.services.grade_service import get_grades_for_student
        
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
        present = sum(1 for a in att if a['status'] == 'Present')
        att_rate = int((present / len(att)) * 100) if att else 100
        
        assignments = get_all_assignments()
        submissions = get_all_submissions()
        sub_ids = {s['assignment_id'] for s in submissions if s['student_id'] == my_uuid}
        due_count = sum(1 for a in assignments if a['id'] not in sub_ids)

        # Graph Data: Performance by Subject
        my_grades = get_grades_for_student(my_uuid)
        # Group by subject and get average score
        perf_data = {}
        for g in my_grades:
            subj = g['subject']
            if subj not in perf_data:
                perf_data[subj] = []
            perf_data[subj].append(g['score'])
        
        graph_labels = list(perf_data.keys())
        graph_values = [sum(scores)/len(scores) for scores in perf_data.values()]

        # Graph Data: Attendance History (Last 7 days)
        att.sort(key=lambda x: x['date'])
        last_7 = att[-7:]
        att_labels = [a['date'] for a in last_7]
        att_values = [1 if a['status'] == 'Present' else 0 for a in last_7]

        return render_template('student_dashboard.html',
                               enrolled_count=enrolled_count,
                               att_rate=att_rate,
                               due_count=due_count,
                               graph_labels=graph_labels,
                               graph_values=graph_values,
                               att_labels=att_labels,
                               att_values=att_values,
                               student_id=my_uuid)

@app.route('/api/students', methods=['GET', 'POST'])
@login_required
def students_api():
    if request.method == 'GET':
        students = get_all_students()
        
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
def grades_api():
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        if not student_id:
            return jsonify({"error": "student_id parameter is required"}), 400
        records = get_grades_for_student(student_id)
        return jsonify(records)
    elif request.method == 'POST':
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
        from src.services.student_service import get_all_students
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
    from src.services.staff_service import get_all_staff
    staff = get_all_staff()
    # Filter for those with role 'Teacher' or 'Professor' (based on staff.json roles)
    professors = [s for s in staff if s['role'] in ['Teacher', 'Professor']]
    return jsonify({"total": len(professors)})

# Subjects
@app.route('/subjects')
@login_required
@admin_required
def subjects_page():
    return render_template('subjects.html')

@app.route('/api/subjects', methods=['GET', 'POST'])
@login_required
def subjects_api():
    if request.method == 'GET':
        return jsonify(get_all_subjects())
    elif request.method == 'POST':
        if current_user.role != 'admin':
            return jsonify({"error": "Unauthorized"}), 403
        data = request.json
        return jsonify(add_subject(data['name'], data['description']))

@app.route('/api/subjects/<subject_id>', methods=['DELETE'])
@login_required
@admin_required
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
        from src.services.student_service import get_all_students
        students = get_all_students()
        me = next((s for s in students if s['email'] == current_user.email), None)
        if me:
            student_uuid = me['student_id']
            
    return render_template('assignments.html', student_uuid=student_uuid)

@app.route('/api/assignments', methods=['GET', 'POST'])
@login_required
def assignments_api():
    if request.method == 'GET':
        return jsonify(get_all_assignments())
    elif request.method == 'POST':
        if current_user.role == 'student':
            return jsonify({"error": "Unauthorized"}), 403
        data = request.json
        # Map user to staff UUID via email
        from src.services.staff_service import get_all_staff
        staff_list = get_all_staff()
        me = next((s for s in staff_list if s['email'] == current_user.email), None)
        my_uuid = me['staff_id'] if me else current_user.id
        
        return jsonify(add_assignment(data['subject'], data['title'], data['description'], data['deadline'], my_uuid))

@app.route('/api/submissions', methods=['GET', 'POST', 'PUT'])
@login_required
def submissions_api():
    if request.method == 'GET':
        return jsonify(get_all_submissions())
    elif request.method == 'POST':
        if current_user.role != 'student':
            return jsonify({"error": "Only students can submit."}), 403
        data = request.json
        # Map user to student UUID via email
        from src.services.student_service import get_all_students
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
