import requests
from src.services.student_service import add_student
from datetime import datetime

def fetch_and_import_dummy_students():
    """Fetches user data from a public API and imports them as students."""
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        response.raise_for_status()
        users = response.json()
        
        imported = []
        today = datetime.now().strftime('%Y-%m-%d')
        
        for user in users:
            # We map API response to our schema
            student = add_student(
                name=user.get('name', 'Unknown'),
                age=20, # Dummy API doesn't have age, default to 20
                email=user.get('email', ''),
                enrollment_date=today
            )
            imported.append(student)
            
        return len(imported)
    except Exception as e:
        print(f"Error fetching API: {e}")
        return 0
