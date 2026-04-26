from src.database import db
from src.models import User
from werkzeug.security import generate_password_hash
import uuid

def get_all_users():
    users = User.query.all()
    # We return the model objects themselves as app.py expects them for LoginManager
    return users

def get_user_by_id(user_id):
    return db.session.get(User, user_id)

def get_user_by_email(email):
    return User.query.filter(User.email.ilike(email)).first()

def create_user(user_id, name, email, password, role):
    # Check if user with same email or same ID exists
    if get_user_by_email(email) or get_user_by_id(user_id):
        return None
        
    user = User(
        id=user_id,
        name=name,
        email=email,
        role=role,
        password_hash=generate_password_hash(password)
    )
    
    db.session.add(user)
    db.session.commit()
    return user

def init_admin_user():
    """Seed original users and student profiles if they don't exist."""
    from src.models import Student
    
    # helper to ensure user exists and has correct info
    def ensure_user(uid, name, email, role):
        u = get_user_by_id(uid)
        if not u:
            create_user(uid, name, email, 'admin123', role)
        else:
            u.name = name
            u.email = email
            u.role = role
            u.password_hash = generate_password_hash('admin123')
            db.session.commit()

    # 1. Admin
    ensure_user('u1', 'Super Admin', 'admin@elitesms.com', 'admin')
    
    # 2. Professors
    ensure_user('u2', 'Dr. Smith', 'professor@elitesms.com', 'professor')
    ensure_user('u5', 'Dr. Jones', 'professor2@elitesms.com', 'professor')
    
    # 3. Students
    from src.models import Student
    
    # Helper to ensure student profile exists and is synced with User ID
    def ensure_student(sid, name, email, age, date, subjects):
        s = db.session.get(Student, sid)
        if not s:
            s = Student(student_id=sid, name=name, email=email, age=age, enrollment_date=date, enrolled_subjects=subjects)
            db.session.add(s)
        else:
            s.name = name
            s.email = email
            s.enrolled_subjects = subjects
        db.session.commit()

    # Find and fix Jane Doe if she exists with a different ID
    s_jane = Student.query.filter_by(email='student1@elitesms.com').first()
    if s_jane and s_jane.student_id != 'u3':
        old_id = s_jane.student_id
        s_jane.student_id = 'u3'
        from src.models import Grade, Attendance, Submission
        Grade.query.filter_by(student_id=old_id).update({Grade.student_id: 'u3'})
        Attendance.query.filter_by(student_id=old_id).update({Attendance.student_id: 'u3'})
        Submission.query.filter_by(student_id=old_id).update({Submission.student_id: 'u3'})
        db.session.commit()

    ensure_student('u3', 'Jane Doe', 'student1@elitesms.com', 20, '2024-01-01', ['Mathematics', 'Physics'])
    ensure_student('u4', 'Student Beta', 'student2@elitesms.com', 21, '2024-01-02', ['Algorithms', 'Data Structures'])

    # 4. Seed Dummy Data for Students if they have none
    from src.models import Grade, Attendance
    
    # Jane Doe (u3) dummy records
    if Grade.query.filter_by(student_id='u3').count() == 0:
        db.session.add(Grade(grade_id='g1', student_id='u3', subject='Mathematics', score=85))
        db.session.add(Grade(grade_id='g2', student_id='u3', subject='Physics', score=78))
        
    if Attendance.query.filter_by(student_id='u3').count() == 0:
        dates = ['2024-04-18', '2024-04-19', '2024-04-20', '2024-04-21', '2024-04-22', '2024-04-23', '2024-04-24']
        for i, d in enumerate(dates):
            status = 'Present' if i != 2 else 'Absent'
            db.session.add(Attendance(attendance_id=f'a{i}', student_id='u3', date=d, status=status))

    # Ensure Staff records match
    from src.models import Staff
    if not Staff.query.get('u2'):
        db.session.add(Staff(staff_id='u2', name='Dr. Smith', email='professor@elitesms.com', role='Teacher', department='Mathematics'))
    if not Staff.query.get('u5'):
        db.session.add(Staff(staff_id='u5', name='Dr. Jones', email='professor2@elitesms.com', role='Teacher', department='Physics'))

    # Seed Assignments
    from src.models import Assignment
    if not Assignment.query.get('as1'):
        db.session.add(Assignment(
            id='as1',
            prof_id='u2',
            subject='Mathematics',
            title='Algebra Fundamentals',
            description='Complete all exercises in Chapter 1.',
            deadline='2024-04-25',
            created_at='2024-04-10T10:00:00'
        ))
    if not Assignment.query.get('as2'):
        db.session.add(Assignment(
            id='as2',
            prof_id='u2',
            subject='Mathematics',
            title='Geometry Basics',
            description='Draw and label 5 geometric shapes.',
            deadline='2024-04-28',
            created_at='2024-04-12T11:00:00'
        ))

    # Seed Quizzes
    from src.models import Quiz, QuizQuestion, QuizOption
    
    # Quiz 1 (Dr. Smith - Math)
    if not Quiz.query.get('q1'):
        q1 = Quiz(id='q1', title='Final Math Exam', subject='Mathematics', prof_id='u2', created_at='2024-04-20 10:00')
        db.session.add(q1)
        questions = [
            ("What is 5 + 7?", ["12", "10", "15", "11"], "12"),
            ("Solve for x: 2x = 10", ["5", "2", "10", "4"], "5"),
            ("Area of a square with side 4?", ["16", "8", "4", "20"], "16"),
            ("Value of Pi (approx)?", ["3.14", "2.14", "4.14", "1.14"], "3.14")
        ]
        for idx, (txt, opts, correct) in enumerate(questions):
            qid = f'q1_q{idx}'
            db.session.add(QuizQuestion(id=qid, quiz_id='q1', question_text=txt))
            for o_txt in opts:
                db.session.add(QuizOption(id=str(uuid.uuid4()), question_id=qid, option_text=o_txt, is_correct=(o_txt == correct)))

    # Quiz 2 (Dr. Jones - Physics)
    if not Quiz.query.get('q2'):
        q2 = Quiz(id='q2', title='Physics Fundamentals', subject='Physics', prof_id='u5', created_at='2024-04-21 11:00')
        db.session.add(q2)
        questions = [
            ("Unit of Force?", ["Newton", "Joule", "Watt", "Volt"], "Newton"),
            ("Speed of light is approx?", ["3x10^8 m/s", "2x10^8 m/s", "1x10^8 m/s", "4x10^8 m/s"], "3x10^8 m/s"),
            ("Force = Mass x ?", ["Acceleration", "Velocity", "Distance", "Time"], "Acceleration"),
            ("Gravity on Earth approx?", ["9.8 m/s^2", "8.8 m/s^2", "10.8 m/s^2", "7.8 m/s^2"], "9.8 m/s^2")
        ]
        for idx, (txt, opts, correct) in enumerate(questions):
            qid = f'q2_q{idx}'
            db.session.add(QuizQuestion(id=qid, quiz_id='q2', question_text=txt))
            for o_txt in opts:
                db.session.add(QuizOption(id=str(uuid.uuid4()), question_id=qid, option_text=o_txt, is_correct=(o_txt == correct)))

    db.session.commit()
    print("Default users, profiles, assignments, and quizzes check complete.")
