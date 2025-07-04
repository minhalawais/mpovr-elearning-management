from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from .websocket_handler import broadcast_content
from datetime import datetime, timedelta
from fastapi import UploadFile, HTTPException
import os
import uuid
from pytz import UTC

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def make_aware(dt):
    return dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Message).order_by(models.Message.created_at.desc()).offset(skip).limit(limit).all()

def get_user_program_id(db: Session, user_id: int) -> Optional[int]:
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return user.program_id if user else None

def get_user_program_messages_with_sender(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    program_id = get_user_program_id(db, user_id)
    if program_id is None:
        return []
    
    messages = db.query(models.Message).filter(models.Message.program_id == program_id).order_by(models.Message.created_at.desc()).offset(skip).limit(limit).all()
    
    serialized_messages = []
    for message in messages:
        message_dict = jsonable_encoder(message)
        sender = db.query(models.User).filter(models.User.user_id == message.sender_id).first()
        message_dict['sender_name'] = sender.username if sender else "Unknown"
        message_dict['role'] = sender.role.value if sender and sender.role else "Unknown"  
        serialized_messages.append(message_dict)
    
    return serialized_messages

async def create_message(db: Session, message: schemas.MessageCreate, sender_id: int) -> dict:
    program_id = get_user_program_id(db, sender_id)
    if program_id is None:
        raise ValueError("User is not associated with any program")
    
    sender = db.query(models.User).filter(models.User.user_id == sender_id).first()
    if not sender:
        raise ValueError("Sender not found")

    db_message = models.Message(
        content=message.content,
        sender_id=sender_id,
        program_id=program_id,
        status=models.MessageStatus.pending
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    message_dict = {
        "message_id": db_message.message_id,
        "content": db_message.content,
        "sender_id": db_message.sender_id,
        "program_id": db_message.program_id,
        "created_at": make_aware(db_message.created_at).isoformat(),
        "updated_at": make_aware(db_message.updated_at).isoformat(),
        "sender_name": sender.username,
        "role": sender.role.value
    }

    await broadcast_content(message_dict, program_id)

    return message_dict

async def create_assignment(db: Session, assignment: schemas.AssignmentCreate, uploaded_file: UploadFile = None):
    uploaded_content_path = None
    if uploaded_file:
        print('Uploaded file:', uploaded_file.filename)
        os.makedirs('uploads', exist_ok=True)
        file_location = f"uploads/{uploaded_file.filename}"
        try:
            with open(file_location, "wb+") as file_object:
                file_object.write(await uploaded_file.read())
            uploaded_content_path = file_location
            print(f"File saved at: {file_location}")
        except Exception as e:
            print(f"Failed to save file: {e}")

    db_assignment = models.Assignment(
        program_id=assignment.program_id,
        description=assignment.description,
        due_date=assignment.due_date,
        uploaded_content=uploaded_content_path,
        week=assignment.week  # Add this line

    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)

    assignment_dict = {
        "id": db_assignment.assignment_id,
        "type": "assignment",
        "title": db_assignment.description[:50],  # Use first 50 chars as title
        "description": db_assignment.description,
        "due_date": make_aware(db_assignment.due_date) if db_assignment.due_date else None,
        "created_at": make_aware(db_assignment.created_at),
        "sender_name": "System",
        "role": "system",
        "link": f"/assignment/{db_assignment.assignment_id}"
    }
    await broadcast_content(assignment_dict, db_assignment.program_id)

    return db_assignment

def get_program_details(db: Session, program_id: int) -> schemas.ProgramDetails:
    program = db.query(models.Program).filter(models.Program.program_id == program_id).first()
    if not program:
        return None
    
    trainees = db.query(models.User, models.Enrollment.start_date).join(
        models.Enrollment, 
        (models.User.user_id == models.Enrollment.user_id) & (models.Enrollment.program_id == program_id)
    ).filter(models.User.role == models.UserRole.learner).all()
    
    trainee_info = [
        schemas.TraineeInfo(
            username=trainee.username,
            enrollment_date=created_at.isoformat() if created_at else None
        )
        for trainee, created_at in trainees
    ]
    
    return schemas.ProgramDetails(
        program_title=program.name,
        total_trainees=len(trainee_info),
        trainees=trainee_info
    )

async def create_quiz(db: Session, quiz: schemas.QuizCreate, user_id: int, program_id: int):
    db_quiz = models.Quiz(
        title=quiz.title,
        description=quiz.description,
        creator_id=user_id,
        program_id=program_id,
        start_date=quiz.start_date,
        end_date=quiz.end_date,
        week=quiz.week,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    questions = []
    for question in quiz.questions:
        db_question = models.QuizQuestion(
            quiz_id=db_quiz.quiz_id,
            text=question.text,
            correct_option=question.correct_option
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        options = []
        for option_text in question.options:
            db_option = models.QuizOption(
                question_id=db_question.question_id,
                text=option_text
            )
            db.add(db_option)
            db.commit()
            db.refresh(db_option)
            options.append(schemas.QuizOptionOut(id=db_option.option_id, text=db_option.text))

        questions.append(schemas.QuizQuestionOut(
            id=db_question.question_id,
            text=db_question.text,
            options=options,
            correct_option=db_question.correct_option
        ))

    db.commit()

    quiz_dict = {
        "id": db_quiz.quiz_id,
        "type": "quiz",
        "title": db_quiz.title,
        "description": db_quiz.description,
        "created_at": make_aware(db_quiz.created_at).isoformat(),
        "sender_name": db_quiz.creator.username,
        "role": db_quiz.creator.role.value,
        "link": f"/quiz/{db_quiz.quiz_id}"
    }
    await broadcast_content(quiz_dict, program_id)

    return schemas.QuizOut(
        id=db_quiz.quiz_id,
        title=db_quiz.title,
        description=db_quiz.description,
        creator_id=db_quiz.creator_id,
        program_id=db_quiz.program_id,
        start_date=db_quiz.start_date,
        end_date=db_quiz.end_date,
        created_at=db_quiz.created_at,
        updated_at=db_quiz.updated_at,
        questions=questions
    )

async def create_content(db: Session, content: schemas.ContentCreate, program_id: int, user_id: int, uploaded_file: UploadFile = None):
    file_path = None
    if uploaded_file and content.content_type != schemas.ContentType.url:
        os.makedirs('uploads', exist_ok=True)
        file_location = f"uploads/{uploaded_file.filename}"
        try:
            with open(file_location, "wb+") as file_object:
                file_object.write(await uploaded_file.read())
            file_path = file_location
            print(f"File saved at: {file_location}")
        except Exception as e:
            print(f"Failed to save file: {e}")

    db_content = models.Content(
        title=content.title,
        content_type=content.content_type,
        description=content.description,
        file_path=file_path,
        program_id=program_id,
        user_id=user_id,
        week=content.week  # Add this line

    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)

    content_dict = {
        "id": db_content.content_id,
        "type": "content",
        "title": db_content.title,
        "description": db_content.description,
        "content_type": db_content.content_type,
        "created_at": make_aware(db_content.created_at),
        "sender_name": db_content.user.username,
        "role": db_content.user.role.value,
        "link": f"/content/{db_content.content_id}"
    }
    await broadcast_content(content_dict, program_id)

    return db_content

async def create_google_meet_session(db: Session, session_data: schemas.VirtualSessionCreate, user: models.User):
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
        
        credentials = Credentials.from_authorized_user_file(
            'D:/PycharmProjects/training-management-app/mpovr_backend/app/config/token.json', 
            SCOPES
        )
        
        service = build('calendar', 'v3', credentials=credentials)
        
        start_time = session_data.scheduled_datetime
        end_time = start_time + timedelta(minutes=session_data.duration_minutes)
        
        meeting_id = str(uuid.uuid4())[:8]
        
        event = {
            'summary': session_data.title,
            'description': session_data.description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC'
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': meeting_id,
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            }
        }
        
        event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()
        
        meeting_link = event.get('hangoutLink', '')
        print('Meeting link:', meeting_link)

        virtual_session = models.VirtualSession(
            title=session_data.title,
            description=session_data.description,
            scheduled_datetime=start_time,
            duration_minutes=session_data.duration_minutes,
            platform="Google Meet",
            meeting_link=meeting_link,
            program_id=user.program_id,
            user_id=user.user_id,
            week=session_data.week  # Add this line

        )
        db.add(virtual_session)
        db.commit()
        db.refresh(virtual_session)
        
        session_dict = {
            "id": virtual_session.session_id,
            "type": "virtual_session",
            "title": virtual_session.title,
            "description": virtual_session.description,
            "scheduled_datetime": make_aware(virtual_session.scheduled_datetime) if virtual_session.scheduled_datetime else None,
            "created_at": make_aware(virtual_session.created_at),
            "sender_name": user.username,
            "role": user.role.value,
            "link": virtual_session.meeting_link
        }
        await broadcast_content(session_dict, user.program_id)

        return virtual_session
    
    except Exception as e:
        db.rollback()
        print(f"Failed to create virtual session: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create virtual session: {str(e)}"
        )


def get_program_content(db: Session, program_id: int, current_week: int, skip: int = 0, limit: int = 100):
    messages = db.query(models.Message).filter(models.Message.program_id == program_id).all()
    quizzes = db.query(models.Quiz).filter(models.Quiz.program_id == program_id, models.Quiz.week <= current_week).all()
    assignments = db.query(models.Assignment).filter(models.Assignment.program_id == program_id, models.Assignment.week <= current_week).all()
    content = db.query(models.Content).filter(models.Content.program_id == program_id, models.Content.week <= current_week).all()
    virtual_sessions = db.query(models.VirtualSession).filter(models.VirtualSession.program_id == program_id, models.VirtualSession.week <= current_week).all()

    all_content = []

    for message in messages:
        all_content.append({
            "id": message.message_id,
            "type": "message",
            "content": message.content,
            "sender_id": message.sender_id,
            "created_at": make_aware(message.created_at),
            "sender_name": message.sender.username,
            "role": message.sender.role.value
        })

    for quiz in quizzes:
        all_content.append({
            "id": quiz.quiz_id,
            "type": "quiz",
            "title": quiz.title,
            "description": quiz.description,
            "created_at": make_aware(quiz.created_at),
            "sender_name": quiz.creator.username,
            "role": quiz.creator.role.value,
            "link": f"/quiz/{quiz.quiz_id}"
        })

    for assignment in assignments:
        all_content.append({
            "id": assignment.assignment_id,
            "type": "assignment",
            "title": assignment.description[:50],  # Use first 50 chars as title
            "description": assignment.description,
            "due_date": make_aware(assignment.due_date) if assignment.due_date else None,
            "created_at": make_aware(assignment.created_at),
            "sender_name": "System",
            "role": "system",
            "link": f"/assignment/{assignment.assignment_id}"
        })

    for content_item in content:
        all_content.append({
            "id": content_item.content_id,
            "type": "content",
            "title": content_item.title,
            "description": content_item.description,
            "content_type": content_item.content_type,
            "created_at": make_aware(content_item.created_at),
            "sender_name": content_item.user.username,
            "role": content_item.user.role.value,
            "link": f"/content/{content_item.content_id}"
        })

    for session in virtual_sessions:
        all_content.append({
            "id": session.session_id,
            "type": "virtual_session",
            "title": session.title,
            "description": session.description,
            "scheduled_datetime": make_aware(session.scheduled_datetime) if session.scheduled_datetime else None,
            "created_at": make_aware(session.created_at),
            "sender_name": session.user.username,
            "role": session.user.role.value,
            "link": session.meeting_link
        })

    sorted_content = sorted(all_content, key=lambda x: x['created_at'], reverse=True)
    return sorted_content[skip : skip + limit]

async def get_quiz_details(db: Session, quiz_id: int):
    quiz = db.query(models.Quiz).filter(models.Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    total_trainees = db.query(models.User).filter(models.User.program_id == quiz.program_id, models.User.role == models.UserRole.learner).count()
    completed_attempts = db.query(models.QuizAttempt).filter(models.QuizAttempt.quiz_id == quiz_id, models.QuizAttempt.end_time.isnot(None)).count()

    return {
        "id": quiz.quiz_id,
        "title": quiz.title,
        "description": quiz.description,
        "start_date": quiz.start_date,
        "end_date": quiz.end_date,
        "total_trainees": total_trainees,
        "completed_attempts": completed_attempts
    }

async def get_assignment_details(db: Session, assignment_id: int):
    assignment = db.query(models.Assignment).filter(models.Assignment.assignment_id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    total_trainees = db.query(models.User).filter(models.User.program_id == assignment.program_id, models.User.role == models.UserRole.learner).count()
    submitted_count = db.query(models.Submission).filter(models.Submission.assignment_id == assignment_id).count()

    return {
        "id": assignment.assignment_id,
        "description": assignment.description,
        "due_date": assignment.due_date,
        "total_trainees": total_trainees,
        "submitted_count": submitted_count
    }

async def get_content_details(db: Session, content_id: int):
    content = db.query(models.Content).filter(models.Content.content_id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    return {
        "id": content.content_id,
        "title": content.title,
        "description": content.description,
        "content_type": content.content_type,
        "file_path": content.file_path
    }

async def get_quizzes(db: Session, program_id: int):
    quizzes = db.query(models.Quiz).filter(models.Quiz.program_id == program_id).all()
    
    quiz_data = []
    for quiz in quizzes:
        total_trainees = db.query(models.User).filter(models.User.program_id == program_id, models.User.role == models.UserRole.learner).count()
        completed_attempts = db.query(models.QuizAttempt).filter(models.QuizAttempt.quiz_id == quiz.quiz_id, models.QuizAttempt.end_time.isnot(None)).count()
        
        quiz_data.append({
            "id": quiz.quiz_id,
            "title": quiz.title,
            "description": quiz.description,
            "start_date": quiz.start_date,
            "end_date": quiz.end_date,
            "total_trainees": total_trainees,
            "completed_attempts": completed_attempts
        })
    
    return quiz_data

async def get_quiz_attempts(db: Session, quiz_id: int):
    attempts = db.query(models.QuizAttempt, models.User.username).join(models.User).filter(models.QuizAttempt.quiz_id == quiz_id).all()
    
    attempt_data = []
    for attempt, username in attempts:
        attempt_data.append({
            "username": username,
            "score": attempt.score,
            "completed_at": attempt.end_time
        })
    
    return attempt_data

async def update_quiz(db: Session, quiz_id: int, quiz_update: schemas.QuizUpdate):
    db_quiz = db.query(models.Quiz).filter(models.Quiz.quiz_id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    for key, value in quiz_update.dict(exclude_unset=True).items():
        setattr(db_quiz, key, value)
    
    db.commit()
    db.refresh(db_quiz)
    return db_quiz
async def get_assignments(db: Session, program_id: int):
    assignments = db.query(models.Assignment).filter(models.Assignment.program_id == program_id).all()
    
    assignment_data = []
    for assignment in assignments:
        total_trainees = db.query(models.User).filter(models.User.program_id == program_id, models.User.role == models.UserRole.learner).count()
        submitted_count = db.query(models.Submission).filter(models.Submission.assignment_id == assignment.assignment_id).count()
        
        assignment_data.append({
            "id": assignment.assignment_id,
            "title": assignment.description,
            "description": assignment.description,
            "due_date": assignment.due_date,
            "total_trainees": total_trainees,
            "submitted_count": submitted_count
        })
    
    return assignment_data

async def get_assignment_submissions(db: Session, assignment_id: int):
    submissions = db.query(models.Submission, models.User.username).join(models.User).filter(models.Submission.assignment_id == assignment_id).all()
    
    submission_data = []
    for submission, username in submissions:
        submission_data.append({
            "username": username,
            "submitted_at": submission.submitted_at,
            "file_path": submission.file_path,
            "grade": submission.grade
        })
    
    return submission_data

async def update_assignment(db: Session, assignment_id: int, assignment_update: schemas.AssignmentUpdate):
    db_assignment = db.query(models.Assignment).filter(models.Assignment.assignment_id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    for key, value in assignment_update.dict(exclude_unset=True).items():
        setattr(db_assignment, key, value)
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

async def grade_assignment(db: Session, assignment_id: int, username: str, grade: int):
    submission = db.query(models.Submission).join(models.User).filter(
        models.Submission.assignment_id == assignment_id,
        models.User.username == username
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    submission.grade = grade
    db.commit()
    db.refresh(submission)
    return submission

async def update_content(db: Session, content_id: int, content_update: schemas.ContentUpdate, file: UploadFile = None):
    db_content = db.query(models.Content).filter(models.Content.content_id == content_id).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    for key, value in content_update.dict(exclude_unset=True).items():
        setattr(db_content, key, value)
    
    if file:
        file_path = await save_file(file)
        db_content.file_path = file_path
    
    db.commit()
    db.refresh(db_content)
    return db_content

# Add this new function to handle file saving
async def save_file(file: UploadFile):
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = f"uploads/{unique_filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return file_path

# Update the get_content_details function
async def get_content_details(db: Session, content_id: int):
    content = db.query(models.Content).filter(models.Content.content_id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    return {
        "id": content.content_id,
        "title": content.title,
        "description": content.description,
        "content_type": content.content_type,
        "file_path": content.file_path,
        "url": content.url
    }

# Update the get_contents function
async def get_contents(db: Session, program_id: int):
    contents = db.query(models.Content).filter(models.Content.program_id == program_id).all()
    
    content_data = []
    for content in contents:
        total_trainees = db.query(models.User).filter(models.User.program_id == program_id, models.User.role == models.UserRole.learner).count()
        viewed_count = db.query(models.ContentView).filter(models.ContentView.content_id == content.content_id).count()
        
        content_data.append({
            "id": content.content_id,
            "title": content.title,
            "description": content.description,
            "content_type": content.content_type,
            "created_at": content.created_at,
            "total_trainees": total_trainees,
            "viewed_count": viewed_count,
            "url": content.url,
            "file_path": content.file_path
        })
    
    return content_data
async def update_program_progress(db: Session, program_id: int, new_week: int) -> schemas.ProgramProgress:
    progress = db.query(models.ProgramProgress).filter(models.ProgramProgress.program_id == program_id).first()
    if not progress:
        progress = models.ProgramProgress(program_id=program_id, current_week=new_week)
        db.add(progress)
    else:
        progress.current_week = new_week
    db.commit()
    db.refresh(progress)
    return schemas.ProgramProgress.from_orm(progress)

async def get_program_progress(db: Session, program_id: int) -> schemas.ProgramProgress:
    progress = db.query(models.ProgramProgress).filter(models.ProgramProgress.program_id == program_id).first()
    if not progress:
        progress = models.ProgramProgress(program_id=program_id, current_week=1)
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return schemas.ProgramProgress.from_orm(progress)
