import sqlite3
import os

db_path = 'student_management.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Students ---")
cursor.execute("SELECT * FROM student")
rows = cursor.fetchall()
for row in rows:
    print(row)

print("\n--- Users ---")
cursor.execute("SELECT * FROM user")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
