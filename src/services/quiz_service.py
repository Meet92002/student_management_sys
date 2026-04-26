import uuid
import random
from datetime import datetime
from src.database import db
from src.models import Quiz, QuizQuestion, QuizOption, QuizResult

def get_all_quizzes(prof_id=None):
    query = Quiz.query
    if prof_id:
        query = query.filter_by(prof_id=prof_id)
    return [q.to_dict() for q in query.all()]

def get_quiz_by_id(quiz_id, shuffle=False):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return None
    
    quiz_data = quiz.to_dict()
    questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
    
    if shuffle:
        random.shuffle(questions)
    
    quiz_data['questions'] = []
    for q in questions:
        q_data = q.to_dict()
        options = QuizOption.query.filter_by(question_id=q.id).all()
        if shuffle:
            random.shuffle(options)
        q_data['options'] = [opt.to_dict() for opt in options]
        quiz_data['questions'].append(q_data)
        
    return quiz_data

def add_quiz(title, subject, prof_id, questions_data):
    quiz_id = str(uuid.uuid4())
    quiz = Quiz(
        id=quiz_id,
        title=title,
        subject=subject,
        prof_id=prof_id,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    db.session.add(quiz)
    
    for q_item in questions_data:
        q_id = str(uuid.uuid4())
        question = QuizQuestion(
            id=q_id,
            quiz_id=quiz_id,
            question_text=q_item['text']
        )
        db.session.add(question)
        
        for opt_item in q_item['options']:
            opt = QuizOption(
                id=str(uuid.uuid4()),
                question_id=q_id,
                option_text=opt_item['text'],
                is_correct=opt_item.get('is_correct', False)
            )
            db.session.add(opt)
            
    db.session.commit()
    return quiz.to_dict()

def submit_quiz_result(quiz_id, student_id, answers):
    """
    answers: dict of {question_id: selected_option_id}
    """
    # Check if already attempted
    existing = QuizResult.query.filter_by(quiz_id=quiz_id, student_id=student_id).first()
    if existing:
        return existing.to_dict()

    quiz = get_quiz_by_id(quiz_id)
    if not quiz:
        return None
    
    score = 0
    total = len(quiz['questions'])
    
    for q in quiz['questions']:
        selected_opt_id = answers.get(q['id'])
        # Find the correct option for this question
        correct_opt = next((opt for opt in q['options'] if opt['is_correct']), None)
        if correct_opt and selected_opt_id == correct_opt['id']:
            score += 1
            
    result = QuizResult(
        id=str(uuid.uuid4()),
        quiz_id=quiz_id,
        student_id=student_id,
        score=score,
        total_questions=total,
        completed_at=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    db.session.add(result)
    db.session.commit()
    return result.to_dict()

def get_quiz_rankings(quiz_id):
    results = QuizResult.query.filter_by(quiz_id=quiz_id).order_by(QuizResult.score.desc()).all()
    # We need student names too, but student_id is enough for now if we map it in the view
    return [r.to_dict() for r in results]

def get_student_quiz_results(student_id):
    results = QuizResult.query.filter_by(student_id=student_id).all()
    return [r.to_dict() for r in results]
