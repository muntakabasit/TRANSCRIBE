from sqlalchemy import create_engine, Column, String, Integer, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TranscriptionJob(Base):
    __tablename__ = "transcription_jobs"
    
    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    language = Column(String, default="en")
    status = Column(String, default="pending")  # pending, processing, completed, failed
    full_text = Column(Text, nullable=True)
    segments = Column(Text, nullable=True)  # JSON string
    detected_language = Column(String, nullable=True)
    detected_mt = Column(String, nullable=True)
    mt_enhanced = Column(Boolean, default=False)
    duration = Column(Float, nullable=True)
    segment_count = Column(Integer, nullable=True)
    processing_time = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
