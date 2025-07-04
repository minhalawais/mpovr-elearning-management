from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, UploadFile
from . import models, schemas
from .auth import get_password_hash
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from .websocket_handler import broadcast_content
from datetime import datetime, timedelta
import os
import uuid
from pytz import UTC
from sqlalchemy import func
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_unique_id(db: Session, enrollment_date: datetime) -> str:
    try:
        count = db.query(models.User).filter(
            func.date(models.User.created_at) == enrollment_date.date()
        ).count()

        year = enrollment_date.year % 100
        month = enrollment_date.month
        day = enrollment_date.day
        sequence = count + 1

        month_str = "ABCDEFGHIJKL"[month - 1]

        return f"{year:02d}{month_str}{day:02d}{sequence:03d}"
    except SQLAlchemyError as e:
        logger.error(f"Database error in generate_unique_id: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate unique ID")
    except Exception as e:
        logger.error(f"Unexpected error in generate_unique_id: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def make_aware(dt):
    return dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt

def get_user(db: Session, user_id: int):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        logger.error(f"Unexpected error in get_user: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_user_by_email(db: Session, email: str):
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_user_by_email: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        logger.error(f"Unexpected error in get_user_by_email: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.User).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")
    except Exception as e:
        logger.error(f"Unexpected error in get_users: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def create_user(db: Session, user: schemas.UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        enrollment_date = datetime.utcnow()
        unique_id = generate_unique_id(db, enrollment_date)
        db_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            unique_id=unique_id,
            created_at=enrollment_date
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error in create_user: {str(e)}")
        raise HTTPException(status_code=400, detail="User with this email or username already exists")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in create_user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in create_user: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_messages(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.Message).order_by(models.Message.created_at.desc()).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_messages: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve messages")
    except Exception as e:
        logger.error(f"Unexpected error in get_messages: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_user_program_id(db: Session, user_id: int) -> Optional[int]:
    try:
        user = db.query(models.User).filter(models.User.user_id == user_id).first()
        return user.program_id if user else None
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_user_program_id: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user program ID")
    except Exception as e:
        logger.error(f"Unexpected error in get_user_program_id: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_user_program_messages_with_sender(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    try:
        program_id = get_user_program_id(db, user_id)
        if program_id is None:
            return []
        
        messages = db.query(models.Message).filter(models.Message.program_id == program_id).order_by(models.Message.created_at.desc()).offset(skip).limit(limit).all()
        
        serialized_messages = []
        for message in messages:
            message_dict = jsonable_encoder(message)
            sender = db.query(models.User).filter(models.User.user_id == message.sender_id).first()
            message_dict['sender_name'] = sender.unique_id if sender else "Unknown"
            message_dict['role'] = sender.role.value if sender and sender.role else "Unknown"  
            serialized_messages.append(message_dict)
        
        return serialized_messages
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_user_program_messages_with_sender: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve program messages")
    except Exception as e:
        logger.error(f"Unexpected error in get_user_program_messages_with_sender: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def create_message(db: Session, message: schemas.MessageCreate, sender_id: int, attachments: List[UploadFile] = None) -> dict:
    try:
        program_id = get_user_program_id(db, sender_id)
        if program_id is None:
            raise ValueError("User is not associated with any program")
        
        sender = db.query(models.User).filter(models.User.user_id == sender_id).first()
        if not sender:
            raise ValueError("Sender not found")

        attachment_paths = []
        attachment_sizes = []
        if attachments:
            for attachment in attachments:
                file_extension = os.path.splitext(attachment.filename)[1]
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                file_location = f"uploads/attachments/{unique_filename}"
                with open(file_location, "wb+") as file_object:
                    file_content = await attachment.read()
                    file_object.write(file_content)
                    file_size = len(file_content)
                attachment_paths.append(file_location)
                attachment_sizes.append(file_size)

        db_message = models.Message(
            content=message.content,
            sender_id=sender_id,
            program_id=program_id,
            status=models.MessageStatus.pending,
            attachments=attachment_paths,
            attachments_size=attachment_sizes
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
            "sender_name": sender.unique_id,
            "role": sender.role.value,
            "attachments": db_message.attachments,
            "attachments_size": db_message.attachments_size,
            "type": "message"
        }

        await broadcast_content(message_dict, program_id)

        return message_dict
    except ValueError as e:
        logger.error(f"Value error in create_message: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in create_message: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create message")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in create_message: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


async def create_assignment(db: Session, assignment: schemas.AssignmentCreate, uploaded_file: UploadFile = None):
    try:
        uploaded_content_path = None
        if uploaded_file:
            print('Uploaded file:', uploaded_file.filename)
            os.makedirs('uploads', exist_ok=True)
            file_location = f"uploads/{uploaded_file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(await uploaded_file.read())
            uploaded_content_path = file_location
            print(f"File saved at: {file_location}")

        db_assignment = models.Assignment(
            program_id=assignment.program_id,
            description=assignment.description,
            due_date=assignment.due_date,
            uploaded_content=uploaded_content_path,
            week=assignment.week
        )
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)

        assignment_dict = {
            "id": db_assignment.assignment_id,
            "type": "assignment",
            "title": db_assignment.description[:50],
            "description": db_assignment.description,
            "due_date": make_aware(db_assignment.due_date) if db_assignment.due_date else None,
            "created_at": make_aware(db_assignment.created_at),
            "sender_name": "System",
            "role": "system",
            "link": f"/assignment/{db_assignment.assignment_id}"
        }
        await broadcast_content(assignment_dict, db_assignment.program_id)

        return db_assignment
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in create_assignment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create assignment")
    except Exception as e:
        logger.error(f"Unexpected error in create_assignment: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_program_details(db: Session, program_id: int) -> schemas.ProgramDetails:
    try:
        program = db.query(models.Program).filter(models.Program.program_id == program_id).first()
        if not program:
            return None
        
        trainees = db.query(models.User, models.Enrollment.start_date).join(
            models.Enrollment, 
            (models.User.user_id == models.Enrollment.user_id) & (models.Enrollment.program_id == program_id)
        ).filter(models.User.role == models.UserRole.learner).all()
        
        trainee_info = [
            schemas.TraineeInfoOut(
                unique_id=trainee.unique_id,
                enrollment_date=created_at.isoformat() if created_at else None
            )
            for trainee, created_at in trainees
        ]
        
        return schemas.ProgramDetails(
            program_title=program.name,
            total_trainees=len(trainee_info),
            trainees=trainee_info,
            start_date=program.start_date.isoformat()
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_program_details: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve program details")
    except Exception as e:
        logger.error(f"Unexpected error in get_program_details: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def create_quiz(db: Session, quiz: schemas.QuizCreate, user_id: int, program_id: int):
    try:
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

        total_trainees = db.query(models.User).filter(models.User.program_id == program_id, models.User.role == models.UserRole.learner).count()

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
            questions=questions,
            week=db_quiz.week,
            total_trainees=total_trainees,
            completed_attempts=0
        )
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error in create_quiz: {str(e)}")
        raise HTTPException(status_code=400, detail="Quiz with this title already exists for this program")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in create_quiz: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create quiz")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in create_quiz: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def create_content(db: Session, content: schemas.ContentCreate, program_id: int, user_id: int, uploaded_file: UploadFile = None):
    try:
        file_path = None
        if uploaded_file and content.content_type != schemas.ContentType.url:
            os.makedirs('uploads', exist_ok=True)
            file_location = f"uploads/{uploaded_file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(await uploaded_file.read())
            file_path = file_location
            print(f"File saved at: {file_location}")

        db_content = models.Content(
            title=content.title,
            content_type=content.content_type,
            description=content.description,
            file_path=file_path,
            program_id=program_id,
            user_id=user_id,
            week=content.week
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
            "sender_name": db_content.user.unique_id,
            "role": db_content.user.role.value,
            "link": f"/content/{db_content.content_id}"
        }
        await broadcast_content(content_dict, program_id)

        return db_content
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in create_content: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create content")
    except Exception as e:
        logger.error(f"Unexpected error in create_content: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def create_virtual_session(db: Session, session_data: schemas.VirtualSessionCreate, user: models.User):
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
            week=session_data.week
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
            "sender_name": user.unique_id,
            "role": user.role.value,
            "link": virtual_session.meeting_link
        }
        await broadcast_content(session_dict, user.program_id)

        return virtual_session
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in create_virtual_session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create virtual session")
    except Exception as e:
        logger.error(f"Unexpected error in create_virtual_session: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_program_content(db: Session, program_id: int, current_week: int, skip: int = 0, limit: int = 100):
    try:
        messages = db.query(models.Message).filter(models.Message.program_id == program_id).all()
        quizzes = db.query(models.Quiz).filter(models.Quiz.program_id == program_id, models.Quiz.week <= current_week).all()
        assignments = db.query(models.Assignment).filter(models.Assignment.program_id == program_id, models.Assignment.week <= current_week).all()
        content = db.query(models.Content).filter(models.Content.program_id == program_id, models.Content.week <= current_week).all()
        virtual_sessions = db.query(models.VirtualSession).filter(models.VirtualSession.program_id == program_id, models.VirtualSession.week <= current_week).all()
        discussions = db.query(models.Discussion).filter(models.Discussion.program_id == program_id, models.Discussion.week <= current_week).all()

        all_content = []

        for message in messages:
            all_content.append({
                "id": message.message_id,
                "type": "message",
                "content": message.content,
                "sender_id": message.sender_id,
                "created_at": make_aware(message.created_at),
                "sender_name": message.sender.unique_id,
                "role": message.sender.role.value,
                "attachments": message.attachments,
                "attachments_size": message.attachments_size
            })

        for quiz in quizzes:
            all_content.append({
                "id": quiz.quiz_id,
                "type": "quiz",
                "title": quiz.title,
                "description": quiz.description,
                "created_at": make_aware(quiz.created_at),
                "sender_name": quiz.creator.unique_id,
                "role": quiz.creator.role.value,
                "link": f"/quiz/{quiz.quiz_id}",
                "week": quiz.week
            })

        for assignment in assignments:
            all_content.append({
                "id": assignment.assignment_id,
                "type": "assignment",
                "title": assignment.description[:50],
                "description": assignment.description,
                "due_date": make_aware(assignment.due_date) if assignment.due_date else None,
                "created_at": make_aware(assignment.created_at),
                "sender_name": "System",
                "role": "system",
                "link": f"/assignment/{assignment.assignment_id}",
                "week": assignment.week
            })

        for content_item in content:
            all_content.append({
                "id": content_item.content_id,
                "type": "content",
                "title": content_item.title,
                "description": content_item.description,
                "content_type": content_item.content_type,
                "created_at": make_aware(content_item.created_at),
                "sender_name": content_item.user.unique_id,
                "role": content_item.user.role.value,
                "link": f"/content/{content_item.content_id}",
                "week": content_item.week
            })

        for session in virtual_sessions:
            all_content.append({
                "id": session.session_id,
                "type": "virtual_session",
                "title": session.title,
                "description": session.description,
                "scheduled_datetime": make_aware(session.scheduled_datetime) if session.scheduled_datetime else None,
                "created_at": make_aware(session.created_at),
                "sender_name": session.user.unique_id,
                "role": session.user.role.value,
                "link": session.meeting_link,
                "week": session.week
            })
        for discussion in discussions:
            all_content.append({
                "id": discussion.discussion_id,
                "type": "discussion",
                "title": discussion.title,
                "description": discussion.description,
                "created_at": make_aware(discussion.created_at),
                "sender_name": discussion.user.unique_id,
                "role": discussion.user.role.value,
                "link": f"/discussion/{discussion.discussion_id}",
                "week": discussion.week
            })

        sorted_content = sorted(all_content, key=lambda x: x['created_at'], reverse=True)
        return sorted_content[skip : skip + limit]
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_program_content: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve program content")
    except Exception as e:
        logger.error(f"Unexpected error in get_program_content: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_quiz_details(db: Session, quiz_id: int):
    try:
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
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_quiz_details: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve quiz details")
    except Exception as e:
        logger.error(f"Unexpected error in get_quiz_details: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_assignment_details(db: Session, assignment_id: int):
    try:
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
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_assignment_details: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve assignment details")
    except Exception as e:
        logger.error(f"Unexpected error in get_assignment_details: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_content_details(db: Session, content_id: int):
    try:
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
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_content_details: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve content details")
    except Exception as e:
        logger.error(f"Unexpected error in get_content_details: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_quizzes(db: Session, program_id: int):
    try:
        quizzes = db.query(models.Quiz).filter(models.Quiz.program_id == program_id).all()
        
        quiz_data = []
        for quiz in quizzes:
            total_trainees = db.query(models.User).filter(models.User.program_id == program_id, models.User.role == models.UserRole.learner).count()
            completed_attempts = db.query(models.QuizAttempt).filter(models.QuizAttempt.quiz_id == quiz.quiz_id, models.QuizAttempt.end_time.isnot(None)).count()
            
            questions = []
            for question in quiz.questions:
                options = [schemas.QuizOptionOut(id=option.option_id, text=option.text) for option in question.options]
                questions.append(schemas.QuizQuestionOut(
                    id=question.question_id,
                    text=question.text,
                    options=options,
                    correct_option=question.correct_option
                ))
            
            quiz_data.append(schemas.QuizOut(
                id=quiz.quiz_id,
                title=quiz.title,
                description=quiz.description,
                start_date=quiz.start_date,
                end_date=quiz.end_date,
                week=quiz.week,
                creator_id=quiz.creator_id,
                program_id=quiz.program_id,
                created_at=quiz.created_at,
                updated_at=quiz.updated_at,
                questions=questions,
                total_trainees=total_trainees,
                completed_attempts=completed_attempts
            ))
        
        return quiz_data
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_quizzes: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve quizzes")
    except Exception as e:
        logger.error(f"Unexpected error in get_quizzes: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_quiz_attempts(db: Session, quiz_id: int):
    try:
        attempts = db.query(models.QuizAttempt, models.User.username).join(models.User).filter(models.QuizAttempt.quiz_id == quiz_id).all()
        
        attempt_data = []
        for attempt, username in attempts:
            attempt_data.append({
                "username": username,
                "score": attempt.score,
                "completed_at": attempt.end_time
            })
        
        return attempt_data
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_quiz_attempts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve quiz attempts")
    except Exception as e:
        logger.error(f"Unexpected error in get_quiz_attempts: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def update_quiz(db: Session, quiz_id: int, quiz_update: schemas.QuizUpdate):
    try:
        db_quiz = db.query(models.Quiz).filter(models.Quiz.quiz_id == quiz_id).first()
        if not db_quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        for key, value in quiz_update.dict(exclude_unset=True).items():
            setattr(db_quiz, key, value)
        
        db.commit()
        db.refresh(db_quiz)
        return db_quiz
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in update_quiz: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update quiz")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in update_quiz: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_assignments(db: Session, program_id: int):
    try:
        assignments = db.query(models.Assignment).filter(models.Assignment.program_id == program_id).all()
        
        assignment_data = []
        for assignment in assignments:
            total_trainees = db.query(models.User).filter(models.User.program_id == program_id, models.User.role == models.UserRole.learner).count()
            submitted_count = db.query(models.Submission).filter(models.Submission.assignment_id == assignment.assignment_id).count()
            
            assignment_data.append(schemas.AssignmentOut(
                id=assignment.assignment_id,
                title=assignment.description,
                description=assignment.description,
                due_date=assignment.due_date,
                total_trainees=total_trainees,
                submitted_count=submitted_count,
                week=assignment.week
            ))
        
        return assignment_data
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_assignments: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve assignments")
    except Exception as e:
        logger.error(f"Unexpected error in get_assignments: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_assignment_submissions(db: Session, assignment_id: int):
    try:
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
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_assignment_submissions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve assignment submissions")
    except Exception as e:
        logger.error(f"Unexpected error in get_assignment_submissions: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def update_assignment(db: Session, assignment_id: int, assignment_update: schemas.AssignmentUpdate):
    try:
        db_assignment = db.query(models.Assignment).filter(models.Assignment.assignment_id == assignment_id).first()
        if not db_assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
        for key, value in assignment_update.dict(exclude_unset=True).items():
            setattr(db_assignment, key, value)
        
        db.commit()
        db.refresh(db_assignment)
        return db_assignment
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in update_assignment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update assignment")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in update_assignment: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def grade_assignment(db: Session, assignment_id: int, unique_id: str, grade: int):
    try:
        submission = db.query(models.Submission).join(models.User).filter(
            models.Submission.assignment_id == assignment_id,
            models.User.unique_id == unique_id
        ).first()

        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        submission.grade = grade
        db.commit()
        db.refresh(submission)
        return submission
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in grade_assignment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to grade assignment")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in grade_assignment: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def update_content(db: Session, content_id: int, content_update: schemas.ContentUpdate, file: UploadFile = None):
    try:
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
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in update_content: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update content")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in update_content: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def save_file(file: UploadFile):
    try:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = f"uploads/{unique_filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return file_path
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save file")

async def get_contents(db: Session, program_id: int):
    try:
        contents = db.query(models.Content).filter(models.Content.program_id == program_id).all()
        
        content_data = []
        for content in contents:
            total_trainees = db.query(models.User).filter(models.User.program_id == program_id, models.User.role == models.UserRole.learner).count()
            viewed_count = db.query(models.ContentView).filter(models.ContentView.content_id == content.content_id).count()
            
            content_data.append(schemas.ContentOut(
                id=content.content_id,
                title=content.title,
                description=content.description,
                content_type=content.content_type,
                created_at=content.created_at,
                total_trainees=total_trainees,
                viewed_count=viewed_count,
                url=content.url,
                file_path=content.file_path,
                week=content.week
            ))
        
        return content_data
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_contents: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve contents")
    except Exception as e:
        logger.error(f"Unexpected error in get_contents: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def create_discussion(db: Session, discussion: schemas.DiscussionCreate, program_id: int, user_id: int, uploaded_file: UploadFile = None):
    try:
        file_path = None
        if uploaded_file:
            file_path = await save_file(uploaded_file)

        db_discussion = models.Discussion(
            title=discussion.title,
            description=discussion.description,
            file_path=file_path,
            program_id=program_id,
            user_id=user_id,
            week=discussion.week
        )
        db.add(db_discussion)
        db.commit()
        db.refresh(db_discussion)

        discussion_dict = {
            "id": db_discussion.discussion_id,
            "type": "discussion",
            "title": db_discussion.title,
            "description": db_discussion.description,
            "created_at": make_aware(db_discussion.created_at),
            "sender_name": db_discussion.user.unique_id,
            "role": db_discussion.user.role.value,
            "link": f"/discussion/{db_discussion.discussion_id}"
        }
        await broadcast_content(discussion_dict, program_id)

        return db_discussion
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in create_discussion: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create discussion")
    except Exception as e:
        logger.error(f"Unexpected error in create_discussion: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_discussions(db: Session, program_id: int):
    try:
        return db.query(models.Discussion).filter(models.Discussion.program_id == program_id).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_discussions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve discussions")
    except Exception as e:
        logger.error(f"Unexpected error in get_discussions: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_discussion(db: Session, discussion_id: int):
    try:
        return db.query(models.Discussion).filter(models.Discussion.discussion_id == discussion_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_discussion: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve discussion")
    except Exception as e:
        logger.error(f"Unexpected error in get_discussion: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def update_discussion(db: Session, discussion_id: int, discussion_update: schemas.DiscussionUpdate):
    try:
        db_discussion = await get_discussion(db, discussion_id)
        if not db_discussion:
            raise HTTPException(status_code=404, detail="Discussion not found")
        
        for key, value in discussion_update.dict(exclude_unset=True).items():
            setattr(db_discussion, key, value)
        
        db.commit()
        db.refresh(db_discussion)
        return db_discussion
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in update_discussion: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update discussion")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in update_discussion: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def create_discussion_reply(db: Session, reply: schemas.DiscussionReplyCreate, discussion_id: int, user_id: int):
    try:
        db_reply = models.DiscussionReply(
            content=reply.content,
            discussion_id=discussion_id,
            user_id=user_id
        )
        db.add(db_reply)
        db.commit()
        db.refresh(db_reply)
        return db_reply
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in create_discussion_reply: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create discussion reply")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in create_discussion_reply: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_discussion_replies(db: Session, discussion_id: int):
    try:
        return db.query(models.DiscussionReply).filter(models.DiscussionReply.discussion_id == discussion_id).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_discussion_replies: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve discussion replies")
    except Exception as e:
        logger.error(f"Unexpected error in get_discussion_replies: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def update_discussion_reply(db: Session, reply_id: int, reply_update: schemas.DiscussionReplyUpdate):
    try:
        db_reply = db.query(models.DiscussionReply).filter(models.DiscussionReply.reply_id == reply_id).first()
        if not db_reply:
            raise HTTPException(status_code=404, detail="Reply not found")
        
        for key, value in reply_update.dict(exclude_unset=True).items():
            setattr(db_reply, key, value)
        
        db.commit()
        db.refresh(db_reply)
        return db_reply
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in update_discussion_reply: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update discussion reply")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in update_discussion_reply: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_program_progress(db: Session, program_id: int) -> schemas.ProgramProgress:
    try:
        progress = db.query(models.ProgramProgress).filter(models.ProgramProgress.program_id == program_id).first()
        if not progress:
            progress = models.ProgramProgress(program_id=program_id, current_week=1)
            db.add(progress)
            db.commit()
            db.refresh(progress)
        return schemas.ProgramProgress.from_orm(progress)
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_program_progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve program progress")
    except Exception as e:
        logger.error(f"Unexpected error in get_program_progress: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_virtual_sessions(db: Session, program_id: int):
    try:
        sessions = db.query(models.VirtualSession).filter(models.VirtualSession.program_id == program_id).all()
        
        for session in sessions:
            total_trainees = db.query(func.count(models.Enrollment.user_id)).filter(
                models.Enrollment.program_id == program_id,
                models.Enrollment.status == models.EnrollmentStatus.active
            ).scalar()
            
            attended_count = db.query(func.count(models.VirtualSessionAttendance.user_id)).filter(
                models.VirtualSessionAttendance.session_id == session.session_id
            ).scalar()
            
            session.total_trainees = total_trainees
            session.attended_count = attended_count
        
        return sessions
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_virtual_sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve virtual sessions")
    except Exception as e:
        logger.error(f"Unexpected error in get_virtual_sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_virtual_session(db: Session, session_id: int):
    try:
        return db.query(models.VirtualSession).filter(models.VirtualSession.session_id == session_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_virtual_session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve virtual session")
    except Exception as e:
        logger.error(f"Unexpected error in get_virtual_session: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def update_virtual_session(db: Session, session_id: int, session_update: schemas.VirtualSessionUpdate, recording_file: UploadFile = None):
    try:
        db_session = db.query(models.VirtualSession).filter(models.VirtualSession.session_id == session_id).first()
        if not db_session:
            raise HTTPException(status_code=404, detail="Virtual session not found")
        
        update_data = session_update.dict(exclude_unset=True)
        
        if recording_file:
            file_location = f"uploads/recordings/{uuid.uuid4()}{os.path.splitext(recording_file.filename)[1]}"
            with open(file_location, "wb+") as file_object:
                file_object.write(recording_file.file.read())
            update_data["recording_url"] = file_location
        
        for key, value in update_data.items():
            setattr(db_session, key, value)
        
        db.commit()
        db.refresh(db_session)
        return db_session
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in update_virtual_session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update virtual session")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in update_virtual_session: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_trainee_attendance(db: Session, session_id: int):
    try:
        attendances = db.query(models.VirtualSessionAttendance).filter(models.VirtualSessionAttendance.session_id == session_id).all()
        return [
            schemas.TraineeAttendance(
                username=attendance.user.unique_id,
                joined_at=attendance.joined_at,
                left_at=attendance.left_at
            ) for attendance in attendances
        ]
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_trainee_attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve trainee attendance")
    except Exception as e:
        logger.error(f"Unexpected error in get_trainee_attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def record_trainee_attendance(db: Session, session_id: int, user_id: int):
    try:
        db_attendance = models.VirtualSessionAttendance(
            session_id=session_id,
            user_id=user_id,
            joined_at=datetime.utcnow()
        )
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in record_trainee_attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to record trainee attendance")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in record_trainee_attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def update_trainee_attendance(db: Session, session_id: int, user_id: int):
    try:
        db_attendance = db.query(models.VirtualSessionAttendance).filter(
            models.VirtualSessionAttendance.session_id == session_id,
            models.VirtualSessionAttendance.user_id == user_id,
            models.VirtualSessionAttendance.left_at == None
        ).first()
        if db_attendance:
            db_attendance.left_at = datetime.utcnow()
            db.commit()
            db.refresh(db_attendance)
        return db_attendance
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in update_trainee_attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update trainee attendance")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in update_trainee_attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_trainer_profile(db: Session, user_id: int) -> Optional[schemas.ProfileOut]:
    try:
        user = db.query(models.User).filter(models.User.user_id == user_id).first()
        if not user or not user.profile:
            return None
        
        profile = user.profile
        return schemas.ProfileOut(
            user_id=user.user_id,
            full_name=profile.full_name,
            email=user.email,
            date_of_birth=profile.date_of_birth,
            phone_number=profile.phone_number,
            address=profile.address,
            education_history=profile.education_history,
            work_experience=profile.work_experience,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_trainer_profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve trainer profile")
    except Exception as e:
        logger.error(f"Unexpected error in get_trainer_profile: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def update_trainer_profile(db: Session, user_id: int, profile_update: schemas.ProfileUpdate) -> Optional[schemas.ProfileOut]:
    try:
        db_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
        if not db_profile:
            return None
        
        update_data = profile_update.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_profile, key, value)
        
        db.commit()
        db.refresh(db_profile)
        return await get_trainer_profile(db, user_id)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in update_trainer_profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update trainer profile")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in update_trainer_profile: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_upcoming_events(db: Session, program_id: int, limit: int = 5):
    try:
        now = datetime.utcnow()
        one_week_from_now = now + timedelta(days=7)

        upcoming_quizzes = db.query(models.Quiz).filter(
            models.Quiz.program_id == program_id,
            models.Quiz.start_date > now,
            models.Quiz.start_date <= one_week_from_now
        ).order_by(models.Quiz.start_date).limit(limit).all()

        upcoming_assignments = db.query(models.Assignment).filter(
            models.Assignment.program_id == program_id,
            models.Assignment.due_date > now,
            models.Assignment.due_date <= one_week_from_now
        ).order_by(models.Assignment.due_date).limit(limit).all()

        upcoming_virtual_sessions = db.query(models.VirtualSession).filter(
            models.VirtualSession.program_id == program_id,
            models.VirtualSession.scheduled_datetime > now,
            models.VirtualSession.scheduled_datetime <= one_week_from_now
        ).order_by(models.VirtualSession.scheduled_datetime).limit(limit).all()

        events = []
        for quiz in upcoming_quizzes:
            events.append(schemas.UpcomingEvent(
                id=quiz.quiz_id,
                title=quiz.title,
                type="quiz",
                datetime=quiz.start_date
            ))

        for assignment in upcoming_assignments:
            events.append(schemas.UpcomingEvent(
                id=assignment.assignment_id,
                title=assignment.description[:50],
                type="assignment",
                datetime=assignment.due_date
            ))

        for session in upcoming_virtual_sessions:
            events.append(schemas.UpcomingEvent(
                id=session.session_id,
                title=session.title,
                type="virtual_session",
                datetime=session.scheduled_datetime
            ))

        return sorted(events, key=lambda x: x.datetime)[:limit]
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_upcoming_events: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve upcoming events")
    except Exception as e:
        logger.error(f"Unexpected error in get_upcoming_events: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def create_message_reply(db: Session, reply: schemas.MessageReplyCreate, sender_id: int) -> dict:
    try:
        program_id = get_user_program_id(db, sender_id)
        if program_id is None:
            raise ValueError("User is not associated with any program")
        
        sender = db.query(models.User).filter(models.User.user_id == sender_id).first()
        if not sender:
            raise ValueError("Sender not found")

        parent_message = db.query(models.Message).filter(models.Message.message_id == reply.parent_id).first()
        if not parent_message:
            raise ValueError("Parent message not found")

        db_reply = models.Message(
            content=reply.content,
            sender_id=sender_id,
            program_id=program_id,
            status=models.MessageStatus.pending,
            parent_id=reply.parent_id
        )
        db.add(db_reply)
        db.commit()
        db.refresh(db_reply)

        reply_dict = {
            "message_id": db_reply.message_id,
            "content": db_reply.content,
            "sender_id": db_reply.sender_id,
            "program_id": db_reply.program_id,
            "created_at": make_aware(db_reply.created_at).isoformat(),
            "updated_at": make_aware(db_reply.updated_at).isoformat(),
            "sender_name": sender.unique_id,
            "role": sender.role.value,
            "parent_id": db_reply.parent_id,

        }

        await broadcast_content(reply_dict, program_id)

        return reply_dict
    except ValueError as e:
        logger.error(f"Value error in create_message_reply: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in create_message_reply: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create message reply")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in create_message_reply: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

