from .database import engine, SessionLocal
from . import models

models.Base.metadata.create_all(bind=engine)