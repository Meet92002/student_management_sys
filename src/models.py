from dataclasses import dataclass, asdict, field

@dataclass
class Student:
    student_id: str
    name: str
    age: int
    email: str
    enrollment_date: str
    enrolled_subjects: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
        
@dataclass
class Grade:
    grade_id: str
    student_id: str
    subject: str
    score: float

    def to_dict(self):
        return asdict(self)

@dataclass
class Attendance:
    attendance_id: str
    student_id: str
    date: str
    status: str

    def to_dict(self):
        return asdict(self)

@dataclass
class Notice:
    notice_id: str
    title: str
    content: str
    date_posted: str
    posted_by: str
    target_roles: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

@dataclass
class Staff:
    staff_id: str
    name: str
    role: str # Teacher, Admin, etc
    department: str

    def to_dict(self):
        return asdict(self)

@dataclass
class Subject:
    subject_id: str
    name: str
    description: str

    def to_dict(self):
        return asdict(self)

@dataclass
class LibraryRecord:
    record_id: str
    student_id: str
    book_title: str
    checkout_date: str
    status: str # Borrowed, Returned

    def to_dict(self):
        return asdict(self)
