#!/usr/bin/env python3
"""
Database handlers for LogLama.

This module provides logging handlers that store log records in a database.
"""

import logging
import threading

from loglama.db.models import LogRecord, create_tables, get_session


class SQLiteHandler(logging.Handler):
    """Logging handler that writes log records to a SQLite database."""

    def __init__(self, level: int = logging.NOTSET):
        super().__init__(level)
        self.lock = threading.RLock()  # type: ignore[assignment]
        # Ensure tables exist
        create_tables()

    def emit(self, record):
        """Store the log record in the database."""
        try:
            # Acquire lock to prevent concurrent database access issues
            with self.lock:
                # Create a new session
                session = get_session()
                try:
                    # Create a LogRecord from the logging.LogRecord
                    log_record = LogRecord.from_log_record(record)

                    # Add and commit to the database
                    session.add(log_record)
                    session.commit()
                except Exception:
                    # Rollback on error
                    session.rollback()
                    raise
                finally:
                    # Always close the session
                    session.close()
        except Exception:
            self.handleError(record)


class AsyncSQLiteHandler(logging.Handler):
    """Asynchronous logging handler that writes log records to a SQLite database."""

    def __init__(
        self, level: int = logging.NOTSET, max_queue_size: int = 1000
    ):
        super().__init__(level)
        self.queue: list[logging.LogRecord] = []  # Queue for storing records
        self.max_queue_size = max_queue_size
        self.lock = threading.RLock()  # type: ignore[assignment]
        self.worker = None
        self.running = False

        # Ensure tables exist
        create_tables()

        # Start the worker thread
        self.start_worker()

    def start_worker(self):
        """Start the worker thread that processes the queue."""
        if self.worker is None or not self.worker.is_alive():
            self.running = True
            self.worker = threading.Thread(
                target=self._process_queue, daemon=True
            )
            self.worker.start()

    def _process_queue(self):
        """Worker thread that processes the queue."""
        while self.running:
            # Process records in batches
            records_to_process = []

            # Get records from the queue
            with self.lock:
                if self.queue:
                    records_to_process = self.queue[:]
                    self.queue = []

            if records_to_process:
                # Process the records
                session = get_session()
                try:
                    for record in records_to_process:
                        log_record = LogRecord.from_log_record(record)
                        session.add(log_record)
                    session.commit()
                except Exception:
                    session.rollback()
                finally:
                    session.close()

            # Sleep to avoid CPU hogging
            import time

            time.sleep(0.1)

    def emit(self, record):
        """Add the log record to the queue."""
        try:
            with self.lock:
                # Add the record to the queue
                self.queue.append(record)

                # If the queue is too large, remove old records
                if len(self.queue) > self.max_queue_size:
                    self.queue = self.queue[-self.max_queue_size :]

                # Ensure the worker is running
                self.start_worker()
        except Exception:
            self.handleError(record)

    def close(self):
        """Stop the worker thread and close the handler."""
        self.running = False
        if self.worker and self.worker.is_alive():
            self.worker.join(1.0)  # Wait for the worker to finish
        super().close()
