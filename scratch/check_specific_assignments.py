import sqlite3
import os

db_path = 'student_management.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM assignment WHERE id='as1' OR id='as2'")
rows = cursor.fetchall()
print(f"Found {len(rows)} matching assignments")
for row in rows:
    print(row)

conn.close()
