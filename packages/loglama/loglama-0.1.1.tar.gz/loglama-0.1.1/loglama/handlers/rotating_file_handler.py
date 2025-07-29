#!/usr/bin/env python3
"""
Enhanced rotating file handler for LogLama.

This module provides an enhanced version of the standard RotatingFileHandler with
additional features like automatic directory creation and improved error handling.
"""

import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union


class EnhancedRotatingFileHandler(RotatingFileHandler):
    """Enhanced version of RotatingFileHandler with additional features."""

    def __init__(
        self,
        filename: Union[str, Path],
        mode: str = "a",
        maxBytes: int = 0,
        backupCount: int = 0,
        encoding: Optional[str] = None,
        delay: bool = False,
        create_dirs: bool = True,
    ):
        """Initialize the handler with the specified parameters.

        Args:
            filename: Path to the log file
            mode: File open mode (default: 'a')
            maxBytes: Maximum file size before rollover (default: 0, no rollover)
            backupCount: Number of backup files to keep (default: 0, no backups)
            encoding: File encoding (default: None)
            delay: Delay file opening until first log record (default: False)
            create_dirs: Create parent directories if they don't exist (default: True)
        """
        # Create parent directories if they don't exist
        if create_dirs:
            log_dir = os.path.dirname(filename)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

        super().__init__(
            filename, mode, maxBytes, backupCount, encoding, delay
        )

    def emit(self, record):
        """Emit a record with improved error handling."""
        try:
            super().emit(record)
        except Exception as e:  # noqa: F841
            # Try to recreate the directory if it doesn't exist
            log_dir = os.path.dirname(self.baseFilename)
            if log_dir and not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir, exist_ok=True)
                    super().emit(record)
                    return
                except Exception:
                    pass

            # If we get here, we couldn't emit the record
            self.handleError(record)
