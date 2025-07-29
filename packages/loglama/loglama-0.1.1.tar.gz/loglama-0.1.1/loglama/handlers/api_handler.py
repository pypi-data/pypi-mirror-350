#!/usr/bin/env python3
"""
API handler for LogLama.

This module provides a handler that sends log records to a remote API endpoint.
"""

import json
import logging
import threading
from queue import Queue
from typing import Any, Dict, Optional

# Try to import requests, but provide a fallback if it's not available
try:
    import requests  # type: ignore[import-untyped]

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class APIHandler(logging.Handler):
    """Handler that sends log records to a remote API endpoint."""

    def __init__(
        self,
        url: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[tuple] = None,
        timeout: float = 5.0,
        max_queue_size: int = 1000,
        batch_size: int = 10,
        level: int = logging.NOTSET,
        async_mode: bool = True,
    ):
        """Initialize the handler with the specified parameters.

        Args:
            url: URL of the API endpoint
            method: HTTP method to use (default: "POST")
            headers: HTTP headers to include in the request (default: None)
            auth: Authentication tuple (username, password) (default: None)
            timeout: Request timeout in seconds (default: 5.0)
            max_queue_size: Maximum number of log records to queue (default: 1000)
            batch_size: Number of log records to send in a batch (default: 10)
            level: Minimum log level to capture (default: NOTSET)
            async_mode: Whether to send log records asynchronously (default: True)
        """
        super().__init__(level=level)

        if not REQUESTS_AVAILABLE:
            raise ImportError(
                "The 'requests' package is required for the APIHandler. "
                "Please install it with 'pip install requests'."
            )

        self.url = url
        self.method = method.upper()
        self.headers = headers or {"Content-Type": "application/json"}
        self.auth = auth
        self.timeout = timeout
        self.max_queue_size = max_queue_size
        self.batch_size = batch_size
        self.async_mode = async_mode

        # Queue for storing log records
        self.queue: Queue = Queue(maxsize=max_queue_size)

        # Start the worker thread if in async mode
        if async_mode:
            self.worker = threading.Thread(target=self._worker, daemon=True)
            self.worker.start()
            self.shutdown_event = threading.Event()

    def emit(self, record):
        """Send the log record to the API endpoint."""
        try:
            # Format the record
            log_data = self._format_record(record)

            if self.async_mode:
                # Add the log record to the queue
                try:
                    self.queue.put_nowait(log_data)
                except Exception:
                    # Queue is full, drop the record
                    self.handleError(record)
            else:
                # Send the log record immediately
                self._send_records([log_data])
        except Exception:
            self.handleError(record)

    def _format_record(self, record) -> Dict[str, Any]:
        """Format the log record as a dictionary."""
        # Format the record
        msg = self.format(record) if self.formatter else record.getMessage()

        # Create the log data dictionary
        log_data = {
            "timestamp": record.created,
            "name": record.name,
            "level": record.levelname,
            "level_no": record.levelno,
            "message": msg,
            "module": record.module,
            "func_name": record.funcName,
            "line_no": record.lineno,
            "process": record.process,
            "process_name": getattr(record, "process_name", "unknown"),
            "thread": record.thread,
            "thread_name": getattr(record, "thread_name", "unknown"),
        }

        # Add exception info if available
        if record.exc_info:
            log_data["exception"] = (
                self.formatter.formatException(record.exc_info)
                if self.formatter
                else logging.Formatter().formatException(record.exc_info)
            )

        # Add context info if available
        if hasattr(record, "context") and record.context:
            try:
                if isinstance(record.context, str):
                    context = json.loads(record.context)
                else:
                    context = record.context
                log_data["context"] = context
            except (json.JSONDecodeError, TypeError):
                log_data["context"] = str(record.context)

        # Add any extra attributes from the record
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
                "context",
                "process_name",
                "thread_name",
            ] and not key.startswith("_"):
                log_data[key] = value

        return log_data

    def _worker(self):
        """Worker thread that sends log records from the queue."""
        records = []

        while not self.shutdown_event.is_set():
            try:
                # Get a record from the queue with a timeout
                record = self.queue.get(timeout=0.1)
                records.append(record)

                # If we have enough records, send them as a batch
                if len(records) >= self.batch_size:
                    self._send_records(records)
                    records = []
            except Exception:
                # Queue is empty or other error, send any records we have
                if records:
                    self._send_records(records)
                    records = []

    def _send_records(self, records):
        """Send a batch of log records to the API endpoint."""
        if not records:
            return

        try:
            # Prepare the request data
            data = {"records": records}

            # Send the request
            response = requests.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                auth=self.auth,
                json=data,
                timeout=self.timeout,
            )

            # Check if the request was successful
            response.raise_for_status()
        except Exception as e:  # noqa: F841
            # Log the error, but don't raise it
            pass

    def flush(self):
        """Flush all pending log records."""
        if self.async_mode:
            # Process all records in the queue
            records = []
            while not self.queue.empty():
                try:
                    record = self.queue.get_nowait()
                    records.append(record)
                except Exception:
                    break

            if records:
                self._send_records(records)

    def close(self):
        """Close the handler and flush all pending log records."""
        if self.async_mode:
            # Signal the worker thread to stop
            self.shutdown_event.set()

            # Wait for the worker thread to finish
            self.worker.join(timeout=5.0)

            # Flush any remaining records
            self.flush()

        super().close()
