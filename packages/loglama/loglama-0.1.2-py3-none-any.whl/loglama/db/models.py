#!/usr/bin/env python3
"""
Database models for LogLama.

This module defines the SQLAlchemy models for storing log records in a database.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import environment loader
from loglama.config.env_loader import get_env

# Get database path from environment or use default
# Ensure we have a valid directory for the database
default_db_dir = Path.home() / ".loglama"
default_db_dir.mkdir(exist_ok=True)
default_db_path = default_db_dir / "loglama.db"

# Get database path from environment or use default
DB_PATH = get_env("LOGLAMA_DB_PATH", str(default_db_path))

# Create the engine
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create the base class for declarative models
Base = declarative_base()


class LogRecord(Base):  # type: ignore[valid-type,misc]
    """Model for storing log records in the database."""

    __tablename__ = "log_records"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    logger_name = Column(String(100))
    level = Column(String(20))
    level_number = Column(Integer)
    message = Column(Text)
    module = Column(String(100))
    function = Column(String(100))
    line_number = Column(Integer)
    process_id = Column(Integer)
    process_name = Column(String(100))
    thread_id = Column(Integer)
    thread_name = Column(String(100))
    exception_info = Column(Text, nullable=True)
    context = Column(Text, nullable=True)

    def __repr__(self):
        return f"<LogRecord(id={self.id}, timestamp={self.timestamp}, level={self.level}, message={self.message[:50]}...)>"  # noqa: E501

    @classmethod
    def from_log_record(cls, record) -> "LogRecord":
        """Create a LogRecord instance from a logging.LogRecord object."""
        # Extract exception info if available
        exception_info = None
        if record.exc_info:
            import traceback

            exception_info = "\n".join(
                traceback.format_exception(*record.exc_info)
            )

        # Extract context info if available
        context_data = None
        if hasattr(record, "context") and record.context:
            if isinstance(record.context, str):
                context_data = record.context
            else:
                context_data = json.dumps(record.context)

        return cls(
            timestamp=datetime.fromtimestamp(record.created),
            logger_name=record.name,
            level=record.levelname,
            level_number=record.levelno,
            message=record.getMessage(),
            module=record.module,
            function=record.funcName,
            line_number=record.lineno,
            process_id=record.process,
            process_name=getattr(
                record, "process_name", f"Process-{record.process}"
            ),
            thread_id=record.thread,
            thread_name=getattr(
                record, "thread_name", f"Thread-{record.thread}"
            ),
            exception_info=exception_info,
            context=context_data,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the log record to a dictionary."""
        result = {
            "id": self.id,
            "timestamp": (
                self.timestamp.isoformat() if self.timestamp else None
            ),
            "logger_name": self.logger_name,
            "level": self.level,
            "level_number": self.level_number,
            "message": self.message,
            "module": self.module,
            "function": self.function,
            "line_number": self.line_number,
            "process_id": self.process_id,
            "process_name": self.process_name,
            "thread_id": self.thread_id,
            "thread_name": self.thread_name,
            "exception_info": self.exception_info,
        }

        # Add context if available
        if self.context:
            try:
                result["context"] = json.loads(self.context)  # type: ignore[arg-type,str]
            except (json.JSONDecodeError, TypeError):
                result["context"] = self.context

        return result


def create_tables() -> None:
    """Create all tables in the database."""
    Base.metadata.create_all(engine)


def get_session():
    """Get a new database session."""
    return Session()
