import sqlite3
import os

db_path = 'student_management.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Submissions ---")
cursor.execute("SELECT * FROM submission")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
