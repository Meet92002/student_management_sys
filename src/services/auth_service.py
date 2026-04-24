import os
from src.utils.file_handler import read_json_file, write_json_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

USERS_FILE = 'users.json'

class User(UserMixin):
    def __init__(self, id, name, email, role, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.password_hash = password_hash

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

def get_all_users():
    return read_json_file(USERS_FILE)

def get_user_by_id(user_id):
    users = get_all_users()
    for u in users:
        if u['id'] == user_id:
            return User(**u)
    return None

def get_user_by_email(email):
    users = get_all_users()
    for u in users:
        if u['email'].lower() == email.lower():
            return User(**u)
    return None

def create_user(user_id, name, email, password, role):
    users = get_all_users()
    
    # Check if exists
    if any(u['email'].lower() == email.lower() for u in users):
        return None
        
    user = User(
        id=user_id,
        name=name,
        email=email,
        role=role,
        password_hash=generate_password_hash(password)
    )
    
    users.append(user.to_dict())
    write_json_file(USERS_FILE, users)
    return user

def init_admin_user():
    """Seed the original Admin if no users exist."""
    users = get_all_users()
    if not users:
        create_user('u1', 'Super Admin', 'admin@elitesms.com', 'admin123', 'admin')
        print("Default Admin user seeded: admin@elitesms.com / admin123")
