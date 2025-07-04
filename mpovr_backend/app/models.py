import uuid
from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Boolean, ForeignKey, Enum, Text, ARRAY
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class UserRole(enum.Enum):
    learner = "learner"
    trainer = "trainer"
    admin = "admin"
    role_admin = "role_admin"

class ApplicationStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class PaymentStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    refunded = "refunded"

class MessageStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ContentType(enum.Enum):
    virtual_live_session = "virtual_live_session"
    video = "video"
    reading = "reading"
    assignment = "assignment"
    practicum = "practicum"
    presentation = "presentation"
    quiz = "quiz"
    document = "document"
    image = "image"
    url = "url"

class EnrollmentStatus(enum.Enum):
    active = "active"
    completed = "completed"
    discontinued = "discontinued"

application_status_enum = Enum(ApplicationStatus, name="application_status", create_type=False)
payment_status_enum = Enum(PaymentStatus, name="payment_status", create_type=False)
message_status_enum = Enum(MessageStatus, name="message_status", create_type=False)
content_type_enum = Enum(ContentType, name="content_type", create_type=False)
enrollment_status_enum = Enum(EnrollmentStatus, name="enrollment_status", create_type=False)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String(8), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    last_login_ip = Column(INET)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255))
    disabled = Column(Boolean, default=False)
    program_id = Column(Integer, ForeignKey("programs.program_id"))

    profile = relationship("Profile", back_populates="user", uselist=False)
    applications = relationship("Application", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    enrollments = relationship("Enrollment", back_populates="user")
    submissions = relationship("Submission", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender")
    agreements = relationship("Agreement", back_populates="user")
    progress = relationship("ProgressTracking", back_populates="user")
    program = relationship("Program", back_populates="users")
    created_quizzes = relationship("Quiz", back_populates="creator")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
    content = relationship("Content", back_populates="user")
    assignments = relationship("Assignment", back_populates="user")
    content_views = relationship("ContentView", back_populates="user")
    virtual_sessions = relationship("VirtualSession", back_populates="user", cascade="all, delete-orphan")
    discussions = relationship("Discussion", back_populates="user")
    discussion_replies = relationship("DiscussionReply", back_populates="user")
    virtual_session_attendances = relationship("VirtualSessionAttendance", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"

    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    full_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    phone_number = Column(String(20))
    address = Column(Text)
    education_history = Column(JSONB)
    work_experience = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="profile")

class Program(Base):
    __tablename__ = "programs"

    program_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    duration = Column(Integer)
    fee = Column(Float(precision=2), nullable=False)
    start_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    assignments = relationship("Assignment", back_populates="program")
    applications = relationship("Application", back_populates="program")
    payments = relationship("Payment", back_populates="program")
    enrollments = relationship("Enrollment", back_populates="program")
    modules = relationship("Module", back_populates="program")
    agreements = relationship("Agreement", back_populates="program")
    messages = relationship("Message", back_populates="program")
    users = relationship("User", back_populates="program")
    quizzes = relationship("Quiz", back_populates="program")
    content = relationship("Content", back_populates="program")
    virtual_sessions = relationship("VirtualSession", back_populates="program", cascade="all, delete-orphan")
    progress = relationship("ProgramProgress", back_populates="program", uselist=False)
    discussions = relationship("Discussion", back_populates="program")

class Application(Base):
    __tablename__ = "applications"

    application_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    program_id = Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"))
    status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.pending)
    interview_slot = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="applications")
    program = relationship("Program", back_populates="applications")

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    program_id = Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"))
    amount = Column(Float(precision=2), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    stripe_payment_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="payments")
    program = relationship("Program", back_populates="payments")

class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    program_id = Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(Enum(EnrollmentStatus), nullable=False, default=EnrollmentStatus.active)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="enrollments")
    program = relationship("Program", back_populates="enrollments")

class Module(Base):
    __tablename__ = "modules"

    module_id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    order_number = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    program = relationship("Program", back_populates="modules")

class Content(Base):
    __tablename__ = "content"

    content_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content_type = Column(String(255), nullable=False)
    description = Column(String(1000))
    file_path = Column(String(255))
    url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    program_id = Column(Integer, ForeignKey("programs.program_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    week = Column(Integer, nullable=False)

    program = relationship("Program", back_populates="content")
    user = relationship("User", back_populates="content")
    content_views = relationship("ContentView", back_populates="content")

class ContentView(Base):
    __tablename__ = "content_views"
    view_id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.content_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    viewed_at = Column(DateTime(timezone=True), server_default=func.now())

    content = relationship("Content", back_populates="content_views")
    user = relationship("User", back_populates="content_views")

class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.program_id"))
    description = Column(Text)
    due_date = Column(DateTime(timezone=True))
    uploaded_content = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.user_id"))
    week = Column(Integer, nullable=False)

    program = relationship("Program", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment")
    user = relationship("User", back_populates="assignments")

class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    file_path = Column(String(255))
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    grade = Column(Float(precision=2))

    assignment = relationship("Assignment", back_populates="submissions")
    user = relationship("User", back_populates="submissions")

class Quiz(Base):
    __tablename__ = "quizzes"

    quiz_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    creator_id = Column(Integer, ForeignKey("users.user_id"))
    program_id = Column(Integer, ForeignKey("programs.program_id"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    week = Column(Integer, nullable=False)

    creator = relationship("User", back_populates="created_quizzes")
    program = relationship("Program", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    question_id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"))
    text = Column(String)
    correct_option = Column(Integer)

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("QuizOption", back_populates="question", cascade="all, delete-orphan")
    responses = relationship("QuizResponse", back_populates="question")

class QuizOption(Base):
    __tablename__ = "quiz_options"

    option_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.question_id"))
    text = Column(String)

    question = relationship("QuizQuestion", back_populates="options")
    responses = relationship("QuizResponse", back_populates="option")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    attempt_id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    score = Column(Float(precision=2))

    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User", back_populates="quiz_attempts")
    responses = relationship("QuizResponse", back_populates="attempt")

class QuizResponse(Base):
    __tablename__ = "quiz_responses"

    response_id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.attempt_id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("quiz_questions.question_id", ondelete="CASCADE"))
    option_id = Column(Integer, ForeignKey("quiz_options.option_id", ondelete="CASCADE"))

    attempt = relationship("QuizAttempt", back_populates="responses")
    question = relationship("QuizQuestion", back_populates="responses")
    option = relationship("QuizOption", back_populates="responses")

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    program_id = Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"))
    content = Column(String, nullable=False)
    status = Column(Enum(MessageStatus), nullable=False, default=MessageStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    parent_id = Column(Integer, ForeignKey("messages.message_id", ondelete="CASCADE"), nullable=True)
    attachments = Column(ARRAY(String), nullable=True)
    attachments_size = Column(ARRAY(Integer), nullable=True)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    program = relationship("Program", back_populates="messages")
    replies = relationship("Message", backref=backref("parent", remote_side=[message_id]))


class Agreement(Base):
    __tablename__ = "agreements"

    agreement_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    program_id = Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"))
    agreement_text = Column(Text, nullable=False)
    signed_at = Column(DateTime(timezone=True))
    docusign_envelope_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="agreements")
    program = relationship("Program", back_populates="agreements")

class ProgressTracking(Base):
    __tablename__ = "progress_tracking"

    progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    content_id = Column(Integer, ForeignKey("content.content_id", ondelete="CASCADE"))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="progress")

class VirtualSession(Base):
    __tablename__ = "virtual_sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    scheduled_datetime = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    platform = Column(String(50), nullable=False, default="Zoom")
    meeting_link = Column(String(255), nullable=False)
    access_code = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    week = Column(Integer, nullable=False)
    attended_count = Column(Integer, nullable=False, default=0)

    program = relationship("Program", back_populates="virtual_sessions")
    user = relationship("User", back_populates="virtual_sessions")
    attendances = relationship("VirtualSessionAttendance", back_populates="session")

class VirtualSessionAttendance(Base):
    __tablename__ = "virtual_session_attendances"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("virtual_sessions.session_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    joined_at = Column(DateTime(timezone=True), nullable=False)
    left_at = Column(DateTime(timezone=True))

    session = relationship("VirtualSession", back_populates="attendances")
    user = relationship("User", back_populates="virtual_session_attendances")

class ProgramProgress(Base):
    __tablename__ = "program_progress"

    progress_id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"), nullable=False)
    current_week = Column(Integer, nullable=False, default=1)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    program = relationship("Program", back_populates="progress")

class Discussion(Base):
    __tablename__ = "discussions"

    discussion_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    file_path = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    program_id = Column(Integer, ForeignKey("programs.program_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    week = Column(Integer, nullable=False)

    program = relationship("Program", back_populates="discussions")
    user = relationship("User", back_populates="discussions")
    replies = relationship("DiscussionReply", back_populates="discussion", cascade="all, delete-orphan")

class DiscussionReply(Base):
    __tablename__ = "discussion_replies"

    reply_id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    discussion_id = Column(Integer, ForeignKey("discussions.discussion_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))

    discussion = relationship("Discussion", back_populates="replies")
    user = relationship("User", back_populates="discussion_replies")

