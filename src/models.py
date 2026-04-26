from src.database import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20))
    password_hash = db.Column(db.String(200))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "password_hash": self.password_hash
        }

class Student(db.Model):
    student_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    enrollment_date = db.Column(db.String(20))
    enrolled_subjects = db.Column(db.JSON, default=[])

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "enrollment_date": self.enrollment_date,
            "enrolled_subjects": self.enrolled_subjects or []
        }

class Grade(db.Model):
    grade_id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50))
    subject = db.Column(db.String(100))
    score = db.Column(db.Float)

    def to_dict(self):
        return {
            "grade_id": self.grade_id,
            "student_id": self.student_id,
            "subject": self.subject,
            "score": self.score
        }

class Attendance(db.Model):
    attendance_id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50))
    date = db.Column(db.String(20))
    status = db.Column(db.String(20))

    def to_dict(self):
        return {
            "attendance_id": self.attendance_id,
            "student_id": self.student_id,
            "date": self.date,
            "status": self.status
        }

class Notice(db.Model):
    notice_id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    date_posted = db.Column(db.String(20))
    posted_by = db.Column(db.String(100))
    target_roles = db.Column(db.JSON, default=[])

    def to_dict(self):
        return {
            "notice_id": self.notice_id,
            "title": self.title,
            "content": self.content,
            "date_posted": self.date_posted,
            "posted_by": self.posted_by,
            "target_roles": self.target_roles or []
        }

class Staff(db.Model):
    staff_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.Column(db.String(50))
    department = db.Column(db.String(100))

    def to_dict(self):
        return {
            "staff_id": self.staff_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "department": self.department
        }

class Subject(db.Model):
    subject_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    department = db.Column(db.String(100))

    def to_dict(self):
        return {
            "subject_id": self.subject_id,
            "name": self.name,
            "description": self.description,
            "department": self.department
        }

class LibraryRecord(db.Model):
    record_id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50))
    book_title = db.Column(db.String(200))
    checkout_date = db.Column(db.String(20))
    status = db.Column(db.String(20))

    def to_dict(self):
        return {
            "record_id": self.record_id,
            "student_id": self.student_id,
            "book_title": self.book_title,
            "checkout_date": self.checkout_date,
            "status": self.status
        }

class Assignment(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    prof_id = db.Column(db.String(50))
    subject = db.Column(db.String(100))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    deadline = db.Column(db.String(20))
    created_at = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "prof_id": self.prof_id,
            "subject": self.subject,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "created_at": self.created_at
        }

class Submission(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    assignment_id = db.Column(db.String(50))
    student_id = db.Column(db.String(50))
    content = db.Column(db.Text)
    submitted_at = db.Column(db.String(50))
    status = db.Column(db.String(20))
    score = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "assignment_id": self.assignment_id,
            "student_id": self.student_id,
            "content": self.content,
            "submitted_at": self.submitted_at,
            "status": self.status,
            "score": self.score
        }

class Quiz(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    prof_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subject": self.subject,
            "prof_id": self.prof_id,
            "created_at": self.created_at
        }

class QuizQuestion(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    quiz_id = db.Column(db.String(50), db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "question_text": self.question_text
        }

class QuizOption(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    question_id = db.Column(db.String(50), db.ForeignKey('quiz_question.id'), nullable=False)
    option_text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "option_text": self.option_text,
            "is_correct": self.is_correct
        }

class QuizResult(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    quiz_id = db.Column(db.String(50), db.ForeignKey('quiz.id'), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "student_id": self.student_id,
            "score": self.score,
            "total_questions": self.total_questions,
            "completed_at": self.completed_at
        }
