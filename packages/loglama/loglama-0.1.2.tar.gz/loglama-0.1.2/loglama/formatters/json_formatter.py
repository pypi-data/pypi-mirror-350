#!/usr/bin/env python3
"""
JSON formatter for LogLama.

This module provides a formatter that outputs log records as JSON strings.
"""

import json
import logging
from typing import Optional


class JSONFormatter(logging.Formatter):
    """Formatter that outputs JSON strings after gathering all the log record info."""

    def __init__(self, datefmt: Optional[str] = None):
        super().__init__(datefmt=datefmt)

    def format(self, record) -> str:
        """Format the log record as a JSON string."""
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "process": record.process,
            "process_name": getattr(record, "process_name", "unknown"),
            "thread": record.thread,
            "thread_name": getattr(record, "thread_name", "unknown"),
        }

        # Add exception info if available
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

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

        return json.dumps(log_data)
