import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd()))

from src.services.auth_service import get_all_users, create_user, USERS_FILE
from src.utils.file_handler import write_json_file
from werkzeug.security import generate_password_hash

def reset_passwords():
    users = [
        {"id": "u1", "name": "Super Admin", "email": "admin@elitesms.com", "password": "admin123", "role": "admin"},
        {"id": "u2", "name": "Prof. Smith", "email": "professor@elitesms.com", "password": "professor123", "role": "professor"},
        {"id": "u3", "name": "Jane Doe", "email": "student@elitesms.com", "password": "student123", "role": "student"}
    ]
    
    new_users_data = []
    for u in users:
        new_users_data.append({
            "id": u["id"],
            "name": u["name"],
            "email": u["email"],
            "role": u["role"],
            "password_hash": generate_password_hash(u["password"])
        })
    
    write_json_file(USERS_FILE, new_users_data)
    print("Passwords reset successfully!")
    print("Admin: admin@elitesms.com / admin123")
    print("Professor: professor@elitesms.com / professor123")
    print("Student: student@elitesms.com / student123")

if __name__ == "__main__":
    reset_passwords()
