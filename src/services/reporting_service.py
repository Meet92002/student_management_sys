import pandas as pd
import numpy as np
from src.database import db
from src.models import Grade, Attendance, Student

def get_grades_dataframe():
    """Reads grades from DB into a pandas DataFrame."""
    try:
        # Use SQL query statement and bind it to the session engine
        query = db.session.query(Grade)
        df = pd.read_sql(query.statement, db.engine)
        if df.empty:
            return pd.DataFrame(columns=['grade_id', 'student_id', 'subject', 'score'])
        return df
    except Exception as e:
        print(f"Error reading grades from DB: {e}")
        return pd.DataFrame(columns=['grade_id', 'student_id', 'subject', 'score'])

def get_subject_performance():
    """Returns numpy-calculated statistics per subject via Pandas."""
    df = get_grades_dataframe()
    if df.empty:
        return []
    
    grouped = df.groupby('subject')['score'].agg([
        ('average', lambda x: float(np.mean(x))),
        ('max', lambda x: float(np.max(x))),
        ('min', lambda x: float(np.min(x)))
    ]).reset_index()
    
    return grouped.to_dict(orient='records')

def get_student_attendance_summary():
    """Returns attendance percentage per student using Pandas and Database."""
    try:
        att_query = db.session.query(Attendance)
        std_query = db.session.query(Student)
        
        att_df = pd.read_sql(att_query.statement, db.engine)
        std_df = pd.read_sql(std_query.statement, db.engine)
        
        if att_df.empty or std_df.empty:
            return []
            
        att_df['is_present'] = att_df['status'].apply(lambda x: 100.0 if x == 'Present' else 0.0)
        
        grouped = att_df.groupby('student_id')['is_present'].mean().reset_index()
        grouped.rename(columns={'is_present': 'attendance_rate'}, inplace=True)
        
        merged = pd.merge(grouped, std_df[['student_id', 'name']], on='student_id', how='left')
        merged = merged.dropna()
        merged = merged.sort_values(by='attendance_rate', ascending=True)
        
        return merged[['name', 'attendance_rate']].to_dict(orient='records')
    except Exception as e:
        print(f"Error generating attendance report: {e}")
        return []
