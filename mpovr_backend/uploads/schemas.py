from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
from typing import Callable

class MessageStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    message_id: int
    sender_id: int
    program_id: int
    created_at: datetime
    updated_at: datetime
    sender_name: str
    role: str  # Add this line

    class Config:
        orm_mode = True
class MessageInput(BaseModel):
    activeTab: str
    messageInput: str
    setMessageInput: Callable
    assignmentDescription: str
    setAssignmentDescription: Callable
    assignmentDueDate: str
    setAssignmentDueDate: Callable
    createAssignment: Callable
    sendMessage: Callable
    quizTitle: str
    setQuizTitle: Callable
    contentTitle: str
    setContentTitle: Callable
    contentDescription: str
    setContentDescription: Callable
    contentType: str
    setContentType: Callable
    virtualSessionTitle: str
    setVirtualSessionTitle: Callable
    virtualSessionDate: str
    setVirtualSessionDate: Callable
    virtualSessionTime: str
    setVirtualSessionTime: Callable
    handleFileChange: Callable
    navigateToPage: Callable

    class Config:
        arbitrary_types_allowed = True
class MessageList(BaseModel):
    messages: List[Message]

class AssignmentBase(BaseModel):
    description: str
    due_date: datetime
    week: int  # Add this line

class AssignmentCreate(BaseModel):
    description: str
    due_date: datetime
    program_id: int
    

class Assignment(AssignmentBase):
    assignment_id: int
    created_at: datetime
    updated_at: datetime
    program_id: int
    uploaded_content: Optional[str]

    class Config:
        orm_mode = True
class TraineeInfo(BaseModel):
    username: str
    enrollment_date: Optional[str]

    @validator('enrollment_date', pre=True)
    def parse_enrollment_date(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value

class ProgramDetails(BaseModel):
    program_title: str
    total_trainees: int
    trainees: List[TraineeInfo]

    class Config:
        orm_mode = True
class QuizOptionCreate(BaseModel):
    text: str

class QuizOptionOut(QuizOptionCreate):
    id: int

    class Config:
        orm_mode = True

class QuizQuestionCreate(BaseModel):
    text: str
    options: List[str]
    correct_option: int

class QuizQuestionOut(BaseModel):
    id: int
    text: str
    options: List[QuizOptionOut]
    correct_option: int

    class Config:
        orm_mode = True

class QuizCreate(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    questions: List[QuizQuestionCreate]

class QuizOut(BaseModel):
    id: int
    title: str
    description: str
    creator_id: int
    program_id: int
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
    questions: List[QuizQuestionOut]

    class Config:
        orm_mode = True

class ContentType(str, Enum):
    video = "video"
    document = "document"
    image = "image"
    url = "url"

class ContentBase(BaseModel):
    title: str
    content_type: ContentType
    description: Optional[str] = None
    file_path: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class Content(ContentBase):
    content_id: int
    program_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
class VirtualSessionCreate(BaseModel):
    title: str
    description: str
    scheduled_datetime: datetime
    duration_minutes: int
    week: int  # Add this line

class ProgramContent(BaseModel):
    id: int
    type: str
    title: Optional[str]
    content: Optional[str]
    description: Optional[str]
    due_date: Optional[datetime]
    scheduled_datetime: Optional[datetime]
    created_at: datetime
    sender_name: str
    role: str
    link: Optional[str]

    class Config:
        orm_mode = True

class QuizBase(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    week: int  # Add this line

class QuizCreate(QuizBase):
    pass

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class QuizOut(QuizBase):
    id: int
    total_trainees: int
    completed_attempts: int

    class Config:
        orm_mode = True

class QuizAttemptOut(BaseModel):
    username: str
    score: float
    completed_at: datetime

    class Config:
        orm_mode = True

class AssignmentBase(BaseModel):
    title: str
    description: str
    due_date: datetime

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class AssignmentOut(AssignmentBase):
    id: int
    total_trainees: int
    submitted_count: int

    class Config:
        orm_mode = True

class AssignmentSubmissionOut(BaseModel):
    username: str
    submitted_at: datetime
    file_path: str
    grade: Optional[int] = None

    class Config:
        orm_mode = True

class GradeSubmission(BaseModel):
    username: str
    grade: int
class ContentBase(BaseModel):
    title: str
    content_type: ContentType
    description: Optional[str] = None
    file_path: Optional[str] = None
    url: Optional[str] = None
    week: int  # Add this line

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: Optional[str] = None
    url: Optional[str] = None

class ContentOut(ContentBase):
    id: int
    created_at: datetime
    total_trainees: int
    viewed_count: int

    class Config:
        orm_mode = True

class ProgramProgress(BaseModel):
    progress_id: int
    program_id: int
    current_week: int
    updated_at: datetime

    class Config:
        orm_mode = True