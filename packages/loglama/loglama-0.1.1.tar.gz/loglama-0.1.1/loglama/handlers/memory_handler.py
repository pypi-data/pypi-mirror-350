#!/usr/bin/env python3
"""
Memory handler for LogLama.

This module provides a handler that stores log records in memory for later retrieval.
"""

import logging
from collections import deque
from typing import Deque, Dict, List, Optional


class MemoryHandler(logging.Handler):
    """Handler that stores log records in memory for later retrieval."""

    def __init__(self, capacity: int = 1000, level: int = logging.NOTSET):
        """Initialize the handler with the specified capacity and level.

        Args:
            capacity: Maximum number of log records to store (default: 1000)
            level: Minimum log level to capture (default: NOTSET)
        """
        super().__init__(level=level)
        self.capacity = capacity
        self.records: Deque[Dict] = deque(maxlen=capacity)

    def emit(self, record):
        """Store the log record in memory."""
        try:
            # Format the record
            msg = (
                self.format(record) if self.formatter else record.getMessage()
            )

            # Store the record with all its attributes
            record_dict = {
                "timestamp": record.created,
                "name": record.name,
                "level": record.levelname,
                "level_no": record.levelno,
                "message": msg,
                "module": record.module,
                "func_name": record.funcName,
                "line_no": record.lineno,
                "process": record.process,
                "thread": record.thread,
                "raw_record": record,
            }

            # Add exception info if available
            if record.exc_info:
                record_dict["exception"] = (
                    self.formatter.formatException(record.exc_info)
                    if self.formatter
                    else logging.Formatter().formatException(record.exc_info)
                )

            # Add context info if available
            if hasattr(record, "context") and record.context:
                record_dict["context"] = record.context

            self.records.append(record_dict)
        except Exception:
            self.handleError(record)

    def get_records(
        self, level: Optional[int] = None, limit: Optional[int] = None
    ) -> List[Dict]:
        """Get stored log records, optionally filtered by level and limited to a certain number.

        Args:
            level: Minimum log level to retrieve (default: None, all levels)
            limit: Maximum number of records to retrieve (default: None, all records)

        Returns:
            List of log record dictionaries
        """
        if level is None:
            filtered_records = list(self.records)
        else:
            filtered_records = [
                r for r in self.records if r["level_no"] >= level
            ]

        if limit is not None and limit > 0:
            return filtered_records[-limit:]

        return filtered_records

    def clear(self):
        """Clear all stored log records."""
        self.records.clear()

    def close(self):
        """Close the handler and clear all stored log records."""
        self.clear()
        super().close()
