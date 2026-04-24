import pandas as pd
import numpy as np
import os
from src.utils.file_handler import get_data_path

def get_grades_dataframe():
    """Reads grades into a pandas DataFrame."""
    filepath = get_data_path('grades.json')
    try:
        # Check if file is empty
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            return pd.DataFrame(columns=['grade_id', 'student_id', 'subject', 'score'])
        df = pd.read_json(filepath)
        if df.empty:
            return pd.DataFrame(columns=['grade_id', 'student_id', 'subject', 'score'])
        return df
    except Exception:
        return pd.DataFrame(columns=['grade_id', 'student_id', 'subject', 'score'])

def get_subject_performance():
    """Returns numpy-calculated statistics per subject via Pandas."""
    df = get_grades_dataframe()
    if df.empty:
        return []
    
    # Using numpy for calculations within pandas aggregations or directly
    grouped = df.groupby('subject')['score'].agg([
        ('average', np.mean),
        ('max', np.max),
        ('min', np.min)
    ]).reset_index()
    
    return grouped.to_dict(orient='records')

def get_student_attendance_summary():
    """Returns attendance percentage per student using Pandas."""
    att_path = get_data_path('attendance.json')
    std_path = get_data_path('students.json')
    
    if not os.path.exists(att_path) or os.path.getsize(att_path) == 0:
        return []
    if not os.path.exists(std_path) or os.path.getsize(std_path) == 0:
        return []
        
    try:
        att_df = pd.read_json(att_path)
        std_df = pd.read_json(std_path)
        
        if att_df.empty or std_df.empty:
            return []
            
        # Group by student_id and calculate percentage of 'Present'
        # Convert Status to a numeric column where Present is 100, else 0
        att_df['is_present'] = att_df['status'].apply(lambda x: 100.0 if x == 'Present' else 0.0)
        
        grouped = att_df.groupby('student_id')['is_present'].mean().reset_index()
        grouped.rename(columns={'is_present': 'attendance_rate'}, inplace=True)
        
        # Merge with students to get names
        merged = pd.merge(grouped, std_df[['student_id', 'name']], on='student_id', how='left')
        merged = merged.dropna() # Remove orphans dynamically for report if any
        
        # Sort by attendance rate ascending so we instantly see lowest attendance
        merged = merged.sort_values(by='attendance_rate', ascending=True)
        
        return merged[['name', 'attendance_rate']].to_dict(orient='records')
    except Exception:
        return []
