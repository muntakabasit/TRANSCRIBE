from pathlib import Path
from datetime import datetime
import logging
import os

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

# ============================================================
# ENV + ENGINE BOOTSTRAP
# ============================================================

# Load .env from project root; fall back to local SQLite file
ENV_PATH = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=ENV_PATH)

DEFAULT_SQLITE = f"sqlite:///{Path(__file__).with_name('dawt_transcriber.db')}"
DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_SQLITE)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TranscriptionJob(Base):
    __tablename__ = "transcription_jobs"

    # ── Original columns ─────────────────────────────────────────────────────
    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    language = Column(String, default="en")
    status = Column(String, default="pending")  # pending, processing, completed, failed
    full_text = Column(Text, nullable=True)
    segments = Column(Text, nullable=True)       # JSON string
    detected_language = Column(String, nullable=True)
    detected_mt = Column(String, nullable=True)
    mt_enhanced = Column(Boolean, default=False)
    duration = Column(Float, nullable=True)
    segment_count = Column(Integer, nullable=True)
    processing_time = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    corrected_text = Column(Text, nullable=True)
    corrected_segments = Column(Text, nullable=True)  # JSON string
    corrected_at = Column(DateTime, nullable=True)

    # ── Background-job contract columns (added via migrate_schema) ────────────
    # All nullable so existing rows load safely without backfill.
    # Readers in main.py use `job.state or job.status`, `job.original_url or
    # job.url`, `job.retry_count or 0`, and `if job.updated_at else None` —
    # so NULL is the correct default for pre-migration rows.
    original_url = Column(String, nullable=True)
    normalized_url = Column(String, nullable=True)
    platform_guess = Column(String, nullable=True)
    state = Column(String, nullable=True)
    retry_count = Column(Integer, nullable=True, default=0)
    updated_at = Column(DateTime, nullable=True)
    failure_code = Column(String, nullable=True)
    failure_message = Column(Text, nullable=True)
    transcription_id = Column(String, nullable=True)


class InstagramCookie(Base):
    __tablename__ = "instagram_cookies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)


# ============================================================
# SCHEMA MIGRATION
# ============================================================

# Each entry: (column_name, ALTER TABLE ADD COLUMN clause)
# All new columns are nullable with no DEFAULT so that SQLite accepts the
# ADD COLUMN even on tables that already have rows. retry_count carries an
# explicit DEFAULT 0 because the runtime reads it as `job.retry_count or 0`
# and a literal default ensures new rows get 0 without an application write.
_MIGRATION_COLUMNS = [
    ("original_url",     "original_url TEXT"),
    ("normalized_url",   "normalized_url TEXT"),
    ("platform_guess",   "platform_guess TEXT"),
    ("state",            "state TEXT"),
    ("retry_count",      "retry_count INTEGER DEFAULT 0"),
    ("updated_at",       "updated_at DATETIME"),
    ("failure_code",     "failure_code TEXT"),
    ("failure_message",  "failure_message TEXT"),
    ("transcription_id", "transcription_id TEXT"),
]


def migrate_schema(bind=None) -> list[str]:
    """
    Idempotently add missing columns to transcription_jobs.

    Safe to call on every startup and on an already-migrated database.
    Returns the list of column names actually added (empty when already up
    to date).  Works for SQLite only; skips gracefully for other engines.
    """
    target = bind or engine
    if not str(target.url).startswith("sqlite"):
        return []

    with target.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(transcription_jobs)"))
        existing = {row[1] for row in result}

    added: list[str] = []
    with target.connect() as conn:
        for col_name, col_def in _MIGRATION_COLUMNS:
            if col_name not in existing:
                conn.execute(
                    text(f"ALTER TABLE transcription_jobs ADD COLUMN {col_def}")
                )
                conn.commit()
                logger.info(f"[migrate_schema] Added column: {col_name}")
                added.append(col_name)

    if not added:
        logger.debug("[migrate_schema] transcription_jobs schema already up to date")
    return added


# ============================================================
# STARTUP
# ============================================================

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.warning(f"Failed to create database tables: {e}")

try:
    migrate_schema()
except Exception as e:
    logger.warning(f"Schema migration failed (non-fatal): {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
