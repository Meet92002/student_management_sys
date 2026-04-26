import sqlite3
import os

db_path = 'student_management.db'
if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_result")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
