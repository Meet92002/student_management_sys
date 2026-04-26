import sqlite3
import os

db_path = 'student_management.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Assignments ---")
cursor.execute("SELECT * FROM assignment")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
