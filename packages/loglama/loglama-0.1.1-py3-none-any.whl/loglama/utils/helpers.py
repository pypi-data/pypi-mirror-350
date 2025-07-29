#!/usr/bin/env python3
"""
Helper functions for LogLama.

This module provides helper functions for configuring and using the logging system.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from loglama.formatters import ColoredFormatter, JSONFormatter
from loglama.handlers import EnhancedRotatingFileHandler, SQLiteHandler
from loglama.utils.filters import ContextFilter

# Try to import structlog, but provide a fallback if it's not available
try:
    import structlog

    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger with the specified name.

    Args:
        name: Name of the logger (default: None, root logger)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def setup_basic_logging(
    level: Union[str, int] = logging.INFO, format_string: Optional[str] = None
):
    """Set up basic logging with console output.

    Args:
        level: Minimum log level to capture (default: INFO)
        format_string: Format string for log messages (default: None, uses a standard format)
    """
    # Convert string level to integer if necessary
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    # Set up the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create a formatter
    if format_string is None:
        format_string = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    formatter = ColoredFormatter(format_string)
    console_handler.setFormatter(formatter)

    # Add a context filter
    context_filter = ContextFilter()
    console_handler.addFilter(context_filter)

    # Add the handler to the root logger
    root_logger.addHandler(console_handler)


def configure_logging(
    name: Optional[str] = None,
    level: Union[str, int] = logging.INFO,
    console: bool = True,
    console_format: Optional[str] = None,
    file: bool = False,
    file_path: Optional[Union[str, Path]] = None,
    file_format: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    database: bool = False,
    db_path: Optional[Union[str, Path]] = None,
    json: bool = False,
    structured: bool = False,
    context_filter: bool = True,
    additional_handlers: Optional[List[logging.Handler]] = None,
    config: Optional[Dict[str, Any]] = None,
) -> logging.Logger:
    """Configure logging with various outputs and formats.

    Args:
        name: Name of the logger (default: None, root logger)
        level: Minimum log level to capture (default: INFO)
        console: Whether to log to the console (default: True)
        console_format: Format string for console log messages (default: None, uses a standard format)
        file: Whether to log to a file (default: False)
        file_path: Path to the log file (default: None, uses a default path)
        file_format: Format string for file log messages (default: None, uses a standard format)
        max_bytes: Maximum size of the log file before rollover (default: 10 MB)
        backup_count: Number of backup files to keep (default: 5)
        database: Whether to log to a database (default: False)
        db_path: Path to the database file (default: None, uses a default path)
        json: Whether to use JSON formatting (default: False)
        structured: Whether to use structured logging with structlog (default: False)
        context_filter: Whether to add a context filter (default: True)
        additional_handlers: Additional handlers to add to the logger (default: None)
        config: Additional configuration options (default: None)

    Returns:
        Configured logger instance
    """
    # Convert string level to integer if necessary
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    # Get the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Use structured logging if requested and available
    if structured and STRUCTLOG_AVAILABLE:
        return _configure_structlog(
            name,
            level,
            console,
            file,
            file_path,
            database,
            db_path,
            json,
            config,
        )

    # Set up console logging
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        if console_format is None:
            console_format = (
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )

        if json:
            formatter = JSONFormatter()
        else:
            formatter = ColoredFormatter(console_format)  # type: ignore[assignment]

        console_handler.setFormatter(formatter)

        if context_filter:
            console_handler.addFilter(ContextFilter())

        logger.addHandler(console_handler)

    # Set up file logging
    if file:
        if file_path is None:
            log_dir = os.environ.get(
                "LOGLAMA_LOG_DIR", os.path.expanduser("~/.loglama/logs")
            )
            os.makedirs(log_dir, exist_ok=True)
            file_path = os.path.join(log_dir, f"{name or 'root'}.log")

        file_handler = EnhancedRotatingFileHandler(
            filename=file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            create_dirs=True,
        )
        file_handler.setLevel(level)

        if file_format is None:
            file_format = (
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )

        if json:
            formatter = JSONFormatter()
        else:
            formatter = logging.Formatter(file_format)  # type: ignore[assignment]

        file_handler.setFormatter(formatter)

        if context_filter:
            file_handler.addFilter(ContextFilter())

        logger.addHandler(file_handler)

    # Set up database logging
    if database:
        if db_path is None:
            db_dir = os.environ.get(
                "LOGLAMA_DB_DIR", os.path.expanduser("~/.loglama/db")
            )
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "loglama.db")

        db_handler = SQLiteHandler(db_path=db_path)
        db_handler.setLevel(level)

        if context_filter:
            db_handler.addFilter(ContextFilter())

        logger.addHandler(db_handler)

    # Add additional handlers
    if additional_handlers:
        for handler in additional_handlers:
            logger.addHandler(handler)

    return logger


def _configure_structlog(
    name, level, console, file, file_path, database, db_path, json, config
):
    """Configure structured logging with structlog.

    This is an internal function used by configure_logging.
    """
    if not STRUCTLOG_AVAILABLE:
        raise ImportError(
            "The 'structlog' package is required for structured logging. "
            "Please install it with 'pip install structlog'."
        )

    # Set up the standard library logger
    stdlib_logger = logging.getLogger(name)
    stdlib_logger.setLevel(level)

    # Clear existing handlers
    for handler in stdlib_logger.handlers:
        stdlib_logger.removeHandler(handler)

    # Set up handlers
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        stdlib_logger.addHandler(console_handler)

    if file:
        if file_path is None:
            log_dir = os.environ.get(
                "LOGLAMA_LOG_DIR", os.path.expanduser("~/.loglama/logs")
            )
            os.makedirs(log_dir, exist_ok=True)
            file_path = os.path.join(log_dir, f"{name or 'root'}.log")

        file_handler = EnhancedRotatingFileHandler(
            filename=file_path,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            create_dirs=True,
        )
        file_handler.setLevel(level)
        stdlib_logger.addHandler(file_handler)

    if database:
        if db_path is None:
            db_dir = os.environ.get(
                "LOGLAMA_DB_DIR", os.path.expanduser("~/.loglama/db")
            )
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "loglama.db")

        db_handler = SQLiteHandler(db_path=db_path)
        db_handler.setLevel(level)
        stdlib_logger.addHandler(db_handler)

    # Configure structlog
    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Create and return the structured logger
    return structlog.get_logger(name)
