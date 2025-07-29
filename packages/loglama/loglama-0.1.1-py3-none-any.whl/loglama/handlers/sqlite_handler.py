#!/usr/bin/env python3
"""
SQLite handler for LogLama.

This module provides a handler that stores log records in a SQLite database.
"""

import json
import logging
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Union


class SQLiteHandler(logging.Handler):
    """Handler that stores log records in a SQLite database."""

    def __init__(
        self, db_path: Union[str, Path], table_name: str = "log_records"
    ):
        """Initialize the handler with the specified database path and table name.

        Args:
            db_path: Path to the SQLite database file
            table_name: Name of the table to store log records in (default: "logs")
        """
        super().__init__()
        self.db_path = Path(db_path)
        self.table_name = table_name

        # Create the directory if it doesn't exist
        os.makedirs(self.db_path.parent, exist_ok=True)

        # Initialize the database
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database by creating the log records table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create the table using the ensure_table_exists method
        self._ensure_table_exists(cursor)

        conn.commit()
        conn.close()

    def _ensure_table_exists(self, cursor):
        """Ensure the logs table exists in the database.

        Args:
            cursor: SQLite cursor to use for executing SQL statements
        """
        # Create the log records table if it doesn't exist
        cursor.execute(
            f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            level_number INTEGER NOT NULL,
            logger_name TEXT NOT NULL,
            message TEXT NOT NULL,
            file_path TEXT,
            line_number INTEGER,
            function TEXT,
            module TEXT,
            process_id INTEGER,
            process_name TEXT,
            thread_id INTEGER,
            thread_name TEXT,
            exception_info TEXT,
            context TEXT
        )
        """
        )

        # Create an index on timestamp and level for faster queries
        cursor.execute(
            f"CREATE INDEX IF NOT EXISTS idx_{self.table_name}_timestamp ON {self.table_name} (timestamp)"
        )
        cursor.execute(
            f"CREATE INDEX IF NOT EXISTS idx_{self.table_name}_level ON {self.table_name} (level_number)"
        )

    def emit(self, record):
        """Store the log record in the database."""
        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Ensure the table exists (in case it was deleted or not created properly)
            self._ensure_table_exists(cursor)

            # Extract context from the record
            context = {}

            # First, check for direct context attributes on the record
            for key, value in record.__dict__.items():
                if key not in [
                    "args",
                    "asctime",
                    "created",
                    "exc_info",
                    "exc_text",
                    "filename",
                    "funcName",
                    "id",
                    "levelname",
                    "levelno",
                    "lineno",
                    "module",
                    "msecs",
                    "message",
                    "msg",
                    "name",
                    "pathname",
                    "process",
                    "processName",
                    "relativeCreated",
                    "stack_info",
                    "thread",
                    "threadName",
                    "process_name",
                    "thread_name",
                ] and not key.startswith("_"):
                    # Add all non-standard attributes to context
                    context[key] = value

            # Then, if there's a context attribute, merge it with our collected context
            if hasattr(record, "context") and record.context:
                if isinstance(record.context, str):
                    try:
                        ctx = json.loads(record.context)
                        context.update(ctx)
                    except (json.JSONDecodeError, TypeError):
                        pass
                elif isinstance(record.context, dict):
                    context.update(record.context)

            # Format exception info if available
            exception = None
            if record.exc_info:
                exception = (
                    self.formatter.formatException(record.exc_info)
                    if self.formatter
                    else logging.Formatter().formatException(record.exc_info)
                )

            # Insert the log record into the database
            cursor.execute(
                f"""
            INSERT INTO {self.table_name} (
                timestamp, level, level_number, logger_name, message, file_path, line_number,
                function, module, process_id, process_name, thread_id, thread_name, exception_info, context
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    datetime.fromtimestamp(record.created).isoformat(),
                    record.levelname,
                    record.levelno,
                    record.name,
                    record.getMessage(),
                    record.pathname,
                    record.lineno,
                    record.funcName,
                    record.module,
                    record.process,
                    getattr(record, "process_name", "unknown"),
                    record.thread,
                    getattr(record, "thread_name", "unknown"),
                    exception if exception else None,
                    json.dumps(context),
                ),
            )

            conn.commit()
            conn.close()
        except Exception as e:  # noqa: F841
            self.handleError(record)

    def close(self):
        """Close the handler."""
        super().close()
