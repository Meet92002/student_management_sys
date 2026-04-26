import sqlite3
import os

db_path = 'student_management.db'

def fix_data():
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Update existing subjects to belong to 'Computer Science'
        cursor.execute("UPDATE subject SET department = 'Computer Science' WHERE department IS NULL")
        conn.commit()
        print("Updated existing subjects to 'Computer Science'.")

    except Exception as e:
        print(f"Update failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_data()
