from typing import List, Optional, Callable
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr,validator
from datetime import date

class MessageStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ContentType(str, Enum):
    video = 'video'
    document = 'document'
    image = 'image'
    url = 'url'

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
    unique_id: str

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    attachments: Optional[List[str]] = None

class Message(MessageBase):
    message_id: int
    sender_id: int
    program_id: int
    created_at: datetime
    updated_at: datetime
    sender_name: str
    role: str
    parent_id: Optional[int] = None
    attachments: Optional[List[str]] = None

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

class MessageReplyCreate(BaseModel):
    content: str
    parent_id: int

class AssignmentBase(BaseModel):
    title: str
    description: str
    due_date: datetime
    week: int

class AssignmentCreate(AssignmentBase):
    program_id: int

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class Assignment(AssignmentBase):
    assignment_id: int
    created_at: datetime
    updated_at: datetime
    program_id: int
    uploaded_content: Optional[str]

    class Config:
        orm_mode = True

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

class TraineeInfo(BaseModel):
    username: str
    enrollment_date: Optional[str]

    @validator('enrollment_date', pre=True)
    def parse_enrollment_date(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value

class TraineeInfoOut(BaseModel):
    unique_id: str
    enrollment_date: Optional[str]

    @validator('enrollment_date', pre=True)
    def parse_enrollment_date(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    class Config:
        orm_mode = True

class ProgramDetails(BaseModel):
    program_title: str
    total_trainees: int
    trainees: List[TraineeInfoOut]
    start_date: str

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

class QuizBase(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    week: int

class QuizCreate(QuizBase):
    questions: List[QuizQuestionCreate]
    week: int

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class QuizOut(QuizBase):
    id: int
    creator_id: int
    program_id: int
    created_at: datetime
    updated_at: datetime
    questions: List[QuizQuestionOut]
    total_trainees: int
    completed_attempts: int
    week: int

    class Config:
        orm_mode = True


class QuizAttemptOut(BaseModel):
    username: str
    score: float
    completed_at: datetime

    class Config:
        orm_mode = True

class ContentBase(BaseModel):
    title: str
    content_type: ContentType
    description: Optional[str] = None
    file_path: Optional[str] = None
    url: Optional[str] = None
    week: int

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: Optional[str] = None
    url: Optional[str] = None

class Content(ContentBase):
    content_id: int
    program_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ContentOut(ContentBase):
    id: int
    created_at: datetime
    total_trainees: int
    viewed_count: int

    class Config:
        orm_mode = True

class VirtualSessionCreate(BaseModel):
    title: str
    description: str
    scheduled_datetime: datetime
    duration_minutes: int
    week: int

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
    week: Optional[int]
    attachments: Optional[List[str]] = None
    attachments_size: Optional[List[int]] = None

    class Config:
        orm_mode = True

class ProgramProgress(BaseModel):
    progress_id: int
    program_id: int
    current_week: int
    updated_at: datetime

    class Config:
        orm_mode = True

class DiscussionBase(BaseModel):
    title: str
    description: str
    week: int

class DiscussionCreate(DiscussionBase):
    pass

class DiscussionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Discussion(DiscussionBase):
    discussion_id: int
    created_at: datetime
    updated_at: datetime
    program_id: int
    user_id: int
    file_path: Optional[str] = None

    class Config:
        orm_mode = True

class DiscussionReplyBase(BaseModel):
    content: str

class DiscussionReplyCreate(DiscussionReplyBase):
    pass

class DiscussionReplyUpdate(BaseModel):
    content: Optional[str] = None

class DiscussionReply(DiscussionReplyBase):
    reply_id: int
    created_at: datetime
    updated_at: datetime
    discussion_id: int
    user_id: int

    class Config:
        orm_mode = True

class ProgramProgress(BaseModel):
    progress_id: int
    program_id: int
    current_week: int
    updated_at: datetime

    class Config:
        orm_mode = True
class VirtualSessionBase(BaseModel):
    title: str
    description: str
    scheduled_datetime: datetime
    duration_minutes: int
    week: int

class VirtualSessionCreate(VirtualSessionBase):
    pass

class VirtualSessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_datetime: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    recording_url: Optional[str] = None

class VirtualSession(BaseModel):
    session_id: int
    title: str
    description: Optional[str]
    scheduled_datetime: datetime
    duration_minutes: int
    meeting_link: str
    week: int
    total_trainees: int
    attended_count: int

    class Config:
        orm_mode = True

class TraineeAttendance(BaseModel):
    username: str
    joined_at: datetime
    left_at: Optional[datetime]

    class Config:
        orm_mode = True

class ProfileBase(BaseModel):
    full_name: str
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    education_history: Optional[dict] = None
    work_experience: Optional[dict] = None

class ProfileUpdate(ProfileBase):
    pass

class ProfileOut(ProfileBase):
    user_id: int
    email: EmailStr
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

class EventType(str, Enum):
    quiz = "quiz"
    assignment = "assignment"
    virtual_session = "virtual_session"

class UpcomingEvent(BaseModel):
    id: int
    title: str
    type: EventType
    datetime: datetime

    class Config:
        orm_mode = True

