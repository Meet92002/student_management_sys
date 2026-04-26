import sqlite3
import os

db_path = 'student_management.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DELETE FROM quiz_result WHERE student_id = 'u3' AND quiz_id IN ('q1', 'q2')")
conn.commit()
print(f"Deleted {cursor.rowcount} rows")
conn.close()
