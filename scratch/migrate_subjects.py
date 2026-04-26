import sqlite3
import os

db_path = 'student_management.db'

def migrate():
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if department column already exists in subject table
        cursor.execute("PRAGMA table_info(subject)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'department' not in columns:
            print("Adding 'department' column to 'subject' table...")
            cursor.execute("ALTER TABLE subject ADD COLUMN department TEXT")
            conn.commit()
            print("Migration successful!")
        else:
            print("'department' column already exists.")

    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
