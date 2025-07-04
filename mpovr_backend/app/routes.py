from fastapi import APIRouter, Depends, HTTPException, status, Query, Form, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth
from .database import get_db
from typing import List, Optional
from datetime import timedelta, datetime
from app.websocket_handler import websocket_endpoint
from fastapi import FastAPI, Depends, WebSocket


router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_endpoint_wrapper(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    await websocket_endpoint(websocket, token, db)


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    print('user:', user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

@router.post("/messages/", response_model=schemas.Message)
def create_message(
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return crud.create_message(db=db, message=message, sender_id=current_user.id)

@router.get("/messages/", response_model=List[schemas.Message])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, skip=skip, limit=limit)
    return messages

from fastapi.encoders import jsonable_encoder

@router.get("/messages/list", response_model=schemas.MessageList)
async def get_messages(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    try:
        messages = crud.get_user_program_messages_with_sender(db, user_id=current_user.user_id, skip=skip, limit=limit)
        return {"messages": messages}
    except Exception as e:
        print(f"Error in get_messages: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/send_messages", response_model=schemas.Message)
async def send_message(
    content: str = Form(...),
    attachments: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        new_message = await crud.create_message(
            db=db,
            message=schemas.MessageCreate(content=content),
            sender_id=current_user.user_id,
            attachments=attachments
        )
        return schemas.Message(**new_message)
    except Exception as e:
        logger.error(f'Error in send_message: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))



from datetime import datetime

@router.get("/program_details", response_model=schemas.ProgramDetails)
async def get_program_details(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    print('current_user:', current_user.role, models.UserRole.trainer)
    if current_user.role != models.UserRole.trainer:
        raise HTTPException(status_code=403, detail="Only trainers can access program details")
    
    program_details = crud.get_program_details(db, current_user.program_id)
    if not program_details:
        raise HTTPException(status_code=404, detail="Program not found")
    
    return program_details

@router.post("/quizzes/", response_model=schemas.QuizOut)
async def create_quiz(
    quiz: schemas.QuizCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        print('current_user:', current_user.program_id)
        return await crud.create_quiz(db, quiz, current_user.user_id, current_user.program_id)
    except Exception as e:
        print(f"Error in create_quiz: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the quiz")


@router.post("/content/", response_model=schemas.Content)
async def create_content(
    title: str = Form(...),
    description: str = Form(...),
    content_type: schemas.ContentType = Form(...),
    week: int = Form(...),
    uploaded_content: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    content_data = schemas.ContentCreate(
        title=title,
        description=description,
        content_type=content_type,
        week=week
    )
    return await crud.create_content(db, content_data, current_user.program_id, current_user.user_id, uploaded_content)


@router.post("/virtual_sessions/create")
async def create_virtual_session(
    session_data: schemas.VirtualSessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        virtual_session = await crud.create_virtual_session(db, session_data, current_user)
        return {"message": "Virtual session created successfully", "meeting_link": virtual_session.meeting_link}
    except Exception as e:
        print(f"Error in create_virtual_session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create virtual session")
@router.get("/program_content", response_model=List[schemas.ProgramContent])
async def get_program_content(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    try:
        progress = await crud.get_program_progress(db, current_user.program_id)
        content = crud.get_program_content(db, current_user.program_id, progress.current_week, skip=skip, limit=limit)
        return content
    except Exception as e:
        print(f"Error in get_program_content: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/quiz/{quiz_id}", response_model=dict)
async def get_quiz_details(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.get_quiz_details(db, quiz_id)

@router.get("/assignments/", response_model=List[schemas.AssignmentOut])
async def get_assignments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.get_assignments(db, current_user.program_id)


@router.get("/content/{content_id}", response_model=dict)
async def get_content_details(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.get_content_details(db, content_id)

@router.get("/quizzes", response_model=List[schemas.QuizOut])
async def get_quizzes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.get_quizzes(db, current_user.program_id)

@router.get("/quiz/{quiz_id}/attempts", response_model=List[schemas.QuizAttemptOut])
async def get_quiz_attempts(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.get_quiz_attempts(db, quiz_id)

@router.put("/quiz/{quiz_id}", response_model=schemas.QuizOut)
async def update_quiz(
    quiz_id: int,
    quiz_update: schemas.QuizUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role != models.UserRole.trainer:
        raise HTTPException(status_code=403, detail="Only trainers can update quizzes")
    return await crud.update_quiz(db, quiz_id, quiz_update)
@router.post("/assignments/", response_model=schemas.Assignment)
async def create_assignment(
    title: str = Form(...),
    description: str = Form(...),
    due_date: str = Form(...),
    week: int = Form(...),
    uploaded_content: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        print('current_user:', current_user.program_id)
        due_date_parsed = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        assignment_data = schemas.AssignmentCreate(
            title=title,
            description=description,
            due_date=due_date_parsed,
            program_id=current_user.program_id,
            week=week
        )
        new_assignment = await crud.create_assignment(db, assignment_data, uploaded_content)
        return new_assignment
    except ValueError as e:
        print('Error in create_assignment:', str(e))
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        print('Error in create_assignment:', str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the assignment: {str(e)}")



@router.get("/assignment/{assignment_id}/submissions", response_model=List[schemas.AssignmentSubmissionOut])
async def get_assignment_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.get_assignment_submissions(db, assignment_id)

@router.put("/assignment/{assignment_id}", response_model=schemas.AssignmentOut)
async def update_assignment(
    assignment_id: int,
    assignment_update: schemas.AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role != models.UserRole.trainer:
        raise HTTPException(status_code=403, detail="Only trainers can update assignments")
    return await crud.update_assignment(db, assignment_id, assignment_update)

@router.post("/assignment/{assignment_id}/grade", response_model=schemas.AssignmentSubmissionOut)
async def grade_assignment(
    assignment_id: int,
    grade_data: schemas.GradeSubmission,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role != models.UserRole.trainer:
        raise HTTPException(status_code=403, detail="Only trainers can grade assignments")
    return await crud.grade_assignment(db, assignment_id, grade_data.unique_id, grade_data.grade)

@router.get("/contents", response_model=List[schemas.ContentOut])
async def get_contents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.get_contents(db, current_user.program_id)


@router.post("/content/{content_id}/views")
async def record_content_view(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.view_content(db, content_id, current_user.user_id)

@router.put("/content/{content_id}", response_model=schemas.ContentOut)
async def update_content(
    content_id: int,
    title: str = Form(...),
    description: str = Form(...),
    content_type: str = Form(...),
    url: Optional[str] = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role != models.UserRole.trainer:
        raise HTTPException(status_code=403, detail="Only trainers can update content")
    
    content_update = schemas.ContentUpdate(
        title=title,
        description=description,
        content_type=content_type,
        url=url
    )
    return await crud.update_content(db, content_id, content_update, file)

@router.post("/discussions/", response_model=schemas.Discussion)
async def create_discussion(
    title: str = Form(...),
    description: str = Form(...),
    week: int = Form(...),
    uploaded_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    discussion_data = schemas.DiscussionCreate(
        title=title,
        description=description,
        week=week
    )
    return await crud.create_discussion(db, discussion_data, current_user.program_id, current_user.user_id, uploaded_file)

@router.get("/discussions/", response_model=List[schemas.Discussion])
async def get_discussions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.get_discussions(db, current_user.program_id)

@router.get("/discussions/{discussion_id}", response_model=schemas.Discussion)
async def get_discussion(
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.get_discussion(db, discussion_id)

@router.put("/discussions/{discussion_id}", response_model=schemas.Discussion)
async def update_discussion(
    discussion_id: int,
    discussion_update: schemas.DiscussionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.update_discussion(db, discussion_id, discussion_update)

@router.post("/discussions/{discussion_id}/replies", response_model=schemas.DiscussionReply)
async def create_discussion_reply(
    discussion_id: int,
    reply: schemas.DiscussionReplyCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.create_discussion_reply(db, reply, discussion_id, current_user.user_id)

@router.get("/discussions/{discussion_id}/replies", response_model=List[schemas.DiscussionReply])
async def get_discussion_replies(
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.get_discussion_replies(db, discussion_id)

@router.put("/discussions/replies/{reply_id}", response_model=schemas.DiscussionReply)
async def update_discussion_reply(
    reply_id: int,
    reply_update: schemas.DiscussionReplyUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.update_discussion_reply(db, reply_id, reply_update)

@router.post("/virtual_sessions/", response_model=schemas.VirtualSession)
async def create_virtual_session(
    session: schemas.VirtualSessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return await crud.create_virtual_session(db, session, current_user.id, current_user.program_id)

@router.get("/virtual_sessions/", response_model=List[schemas.VirtualSession])
async def get_virtual_sessions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return crud.get_virtual_sessions(db, current_user.program_id)

@router.get("/virtual_sessions/{session_id}", response_model=schemas.VirtualSession)
async def get_virtual_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    session = crud.get_virtual_session(db, session_id)
    if not session or session.program_id != current_user.program_id:
        raise HTTPException(status_code=404, detail="Virtual session not found")
    return session

@router.put("/virtual_sessions/{session_id}", response_model=schemas.VirtualSession)
async def update_virtual_session(
    session_id: int,
    session_update: schemas.VirtualSessionUpdate,
    recording_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    session = crud.get_virtual_session(db, session_id)
    if not session or session.program_id != current_user.program_id:
        raise HTTPException(status_code=404, detail="Virtual session not found")
    return await crud.update_virtual_session(db, session_id, session_update, recording_file)

@router.get("/virtual_session/{session_id}/attendance", response_model=List[schemas.TraineeAttendance])
async def get_trainee_attendance(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    session = crud.get_virtual_session(db, session_id)
    if not session or session.program_id != current_user.program_id:
        raise HTTPException(status_code=404, detail="Virtual session not found")
    return crud.get_trainee_attendance(db, session_id)

@router.post("/virtual_sessions/{session_id}/join")
async def join_virtual_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    session = crud.get_virtual_session(db, session_id)
    if not session or session.program_id != current_user.program_id:
        raise HTTPException(status_code=404, detail="Virtual session not found")
    crud.record_trainee_attendance(db, session_id, current_user.id)
    return {"message": "Joined the virtual session successfully"}

@router.post("/virtual_sessions/{session_id}/leave")
async def leave_virtual_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    session = crud.get_virtual_session(db, session_id)
    if not session or session.program_id != current_user.program_id:
        raise HTTPException(status_code=404, detail="Virtual session not found")
    crud.update_trainee_attendance(db, session_id, current_user.id)
    return {"message": "Left the virtual session successfully"}


@router.get("/profile", response_model=schemas.ProfileOut)
async def get_trainer_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role != models.UserRole.trainer:
        raise HTTPException(status_code=403, detail="Only trainers can access this endpoint")
    
    profile = await crud.get_trainer_profile(db, current_user.user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/profile", response_model=schemas.ProfileOut)
async def update_trainer_profile(
    profile_update: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role != models.UserRole.trainer:
        raise HTTPException(status_code=403, detail="Only trainers can update their profile")
    
    updated_profile = await crud.update_trainer_profile(db, current_user.user_id, profile_update)
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated_profile

@router.get("/upcoming_events", response_model=List[schemas.UpcomingEvent])
async def get_upcoming_events(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
    limit: int = Query(5, ge=1, le=10)
):
    return await crud.get_upcoming_events(db, current_user.program_id, limit)

@router.post("/reply_message", response_model=schemas.Message)
async def reply_message(
    reply: schemas.MessageReplyCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        new_reply = await crud.create_message_reply(db=db, reply=reply, sender_id=current_user.user_id)
        return schemas.Message(**new_reply)
    except Exception as e:
        print('Error in reply_message:', str(e))
        raise HTTPException(status_code=500, detail=str(e))