import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import app
from src.models import Student, User

def verify():
    with app.app_context():
        try:
            student_count = Student.query.count()
            user_count = User.query.count()
            print(f"Database verification successful!")
            print(f"Students in DB: {student_count}")
            print(f"Users in DB: {user_count}")
            
            # Check if admin user exists
            admin = User.query.filter_by(email='admin@elitesms.com').first()
            if admin:
                print(f"Admin user found: {admin.name}")
            else:
                print("Admin user NOT found!")
                
            return True
        except Exception as e:
            print(f"Verification failed: {e}")
            return False

if __name__ == "__main__":
    verify()
