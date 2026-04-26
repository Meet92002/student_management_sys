import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import app
from src.models import Subject, Staff

def check_data():
    with app.app_context():
        print("--- Subjects ---")
        subjects = Subject.query.all()
        for s in subjects:
            print(f"ID: {s.subject_id}, Name: {s.name}")
        
        print("\n--- Staff ---")
        staff_members = Staff.query.all()
        for st in staff_members:
            print(f"ID: {st.staff_id}, Name: {st.name}, Email: {st.email}, Dept: {st.department}")

if __name__ == "__main__":
    check_data()
