#!/usr/bin/env python3
"""
Simplified logging interface for LogLama.

This module provides a simplified interface for using LogLama in different files,
without the need to specify class names or contexts. It automatically captures
context information and provides decorator support.
"""

import functools
import inspect
import os
import socket
import sys
import time
from typing import Optional

from loglama.core.env_manager import load_central_env
from loglama.core.logger import get_logger, setup_logging

# Initialize environment and logging
load_central_env()
setup_logging()

# Global context that will be automatically included in all log messages
_global_context = {
    "hostname": socket.gethostname(),
    "pid": os.getpid(),
    "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
}


def set_global_context(**kwargs):
    """
    Set global context values that will be included in all log messages.

    Args:
        **kwargs: Key-value pairs to add to the global context.
    """
    _global_context.update(kwargs)


def get_global_context():
    """
    Get the current global context.

    Returns:
        Dict: The current global context.
    """
    return _global_context.copy()


def _get_caller_info():
    """
    Get information about the caller of the logging function.

    Returns:
        Dict: Information about the caller (module, function, line number).
    """
    frame = inspect.currentframe()
    # Go up 3 frames to get the caller of the logging function
    # (1: this function, 2: log function, 3: caller)
    for _ in range(3):
        if frame.f_back is not None:
            frame = frame.f_back
        else:
            break

    module = inspect.getmodule(frame)
    module_name = module.__name__ if module else "unknown"
    function_name = frame.f_code.co_name if frame else "unknown"
    line_number = frame.f_lineno if frame else 0

    # Use non-conflicting names to avoid overwriting reserved LogRecord attributes
    return {
        "caller_module": module_name,
        "caller_function": function_name,
        "caller_line": line_number,
    }


def log(level: str, message: str, logger_name: Optional[str] = None, **kwargs):
    """
    Log a message with the specified level and automatically include context information.

    Args:
        level: The log level (debug, info, warning, error, critical).
        message: The log message.
        logger_name: Optional name for the logger. If not provided, it will be determined automatically.
        **kwargs: Additional context to include in the log message.
    """
    # Get caller information
    caller_info = _get_caller_info()

    # Determine logger name if not provided
    if logger_name is None:
        logger_name = caller_info["caller_module"]

    # Get logger
    logger = get_logger(logger_name)

    # Combine global context, caller info, and provided kwargs
    context = {**_global_context, **caller_info, **kwargs}

    # Log the message with the combined context
    getattr(logger, level.lower())(message, extra=context)


def debug(message: str, logger_name: Optional[str] = None, **kwargs):
    """
    Log a debug message with automatic context.

    Args:
        message: The log message.
        logger_name: Optional name for the logger. If not provided, it will be determined automatically.
        **kwargs: Additional context to include in the log message.
    """
    log("debug", message, logger_name, **kwargs)


def info(message: str, logger_name: Optional[str] = None, **kwargs):
    """
    Log an info message with automatic context.

    Args:
        message: The log message.
        logger_name: Optional name for the logger. If not provided, it will be determined automatically.
        **kwargs: Additional context to include in the log message.
    """
    log("info", message, logger_name, **kwargs)


def warning(message: str, logger_name: Optional[str] = None, **kwargs):
    """
    Log a warning message with automatic context.

    Args:
        message: The log message.
        logger_name: Optional name for the logger. If not provided, it will be determined automatically.
        **kwargs: Additional context to include in the log message.
    """
    log("warning", message, logger_name, **kwargs)


def error(message: str, logger_name: Optional[str] = None, **kwargs):
    """
    Log an error message with automatic context.

    Args:
        message: The log message.
        logger_name: Optional name for the logger. If not provided, it will be determined automatically.
        **kwargs: Additional context to include in the log message.
    """
    log("error", message, logger_name, **kwargs)


def critical(message: str, logger_name: Optional[str] = None, **kwargs):
    """
    Log a critical message with automatic context.

    Args:
        message: The log message.
        logger_name: Optional name for the logger. If not provided, it will be determined automatically.
        **kwargs: Additional context to include in the log message.
    """
    log("critical", message, logger_name, **kwargs)


def exception(
    message: str,
    logger_name: Optional[str] = None,
    exc_info: bool = True,
    **kwargs,
):
    """Log an exception with traceback."""
    caller_info = _get_caller_info()
    if not logger_name:
        logger_name = caller_info["caller_module"]

    logger = get_logger(logger_name)
    context = {**caller_info, **_global_context, **kwargs}

    # Don't pass exc_info in extra context as it's a reserved attribute
    # Instead, pass it directly to the logger.error method
    logger.error(message, exc_info=exc_info, extra=context)


def timed(
    func=None,
    *,
    name: Optional[str] = None,
    level: str = "info",
    logger_name: Optional[str] = None,
):
    """
    Decorator to time the execution of a function and log the result.

    Args:
        func: The function to decorate.
        name: Optional name for the timer. If not provided, the function name will be used.
        level: The log level to use for the timing message.
        logger_name: Optional name for the logger. If not provided, it will be determined automatically.

    Returns:
        The decorated function.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timer_name = name or func.__name__
            start_time = time.time()

            # Get caller information
            caller_info = _get_caller_info()

            # Determine logger name if not provided
            nonlocal logger_name
            if logger_name is None:
                logger_name = caller_info["caller_module"]

            # Log start message
            log(
                level,
                f"Starting {timer_name}",
                logger_name,
                operation=timer_name,
                status="started",
            )

            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time

                # Log completion message
                log(
                    level,
                    f"Completed {timer_name} in {elapsed:.3f} seconds",
                    logger_name,
                    operation=timer_name,
                    status="completed",
                    duration=elapsed,
                )

                return result
            except Exception as e:
                elapsed = time.time() - start_time

                # Log error message
                log(
                    "error",
                    f"Error in {timer_name} after {elapsed:.3f} seconds: {str(e)}",
                    logger_name,
                    operation=timer_name,
                    status="error",
                    duration=elapsed,
                    error=str(e),
                )

                raise

        return wrapper

    if func is None:
        return decorator
    return decorator(func)


def logged(
    func=None,
    *,
    level: str = "info",
    logger_name: Optional[str] = None,
    log_args: bool = True,
    log_result: bool = True,
    comment: Optional[str] = None,
):
    """
    Decorator to log function calls, arguments, and results.

    Args:
        func: The function to decorate.
        level: The log level to use for the log messages.
        logger_name: Optional name for the logger. If not provided, it will be determined automatically.
        log_args: Whether to log the function arguments.
        log_result: Whether to log the function result.
        comment: Optional comment to include in the log message.

    Returns:
        The decorated function.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get caller information
            caller_info = _get_caller_info()

            # Determine logger name if not provided
            nonlocal logger_name
            if logger_name is None:
                logger_name = caller_info["caller_module"]

            # Prepare context
            context = {"func_name": func.__name__}
            if comment:
                context["comment"] = comment

            # Log arguments if requested
            if log_args:
                # Convert args to a safe string representation
                args_str = ", ".join([repr(arg) for arg in args])
                kwargs_str = ", ".join(
                    [f"{k}={repr(v)}" for k, v in kwargs.items()]
                )
                args_repr = f"({args_str}{', ' if args_str and kwargs_str else ''}{kwargs_str})"
                context["func_args"] = args_repr

            # Log function call
            log(
                level,
                f"Calling {func.__name__}{' - ' + comment if comment else ''}",
                logger_name,
                **context,
            )

            try:
                result = func(*args, **kwargs)

                # Log result if requested
                if log_result:
                    try:
                        result_repr = repr(result)
                        if len(result_repr) > 1000:  # Truncate long results
                            result_repr = result_repr[:997] + "..."
                        context["func_result"] = result_repr
                    except Exception:
                        context["func_result"] = "<unprintable>"

                log(
                    level,
                    f"Completed {func.__name__}{' - ' + comment if comment else ''}",
                    logger_name,
                    status="completed",
                    **context,
                )

                return result
            except Exception as e:
                log(
                    "error",
                    f"Error in {func.__name__}: {str(e)}{' - ' + comment if comment else ''}",
                    logger_name,
                    status="error",
                    error=str(e),
                    **context,
                )
                raise

        return wrapper

    if func is None:
        return decorator
    return decorator(func)


def configure_db_logging(db_path: str, table_name: Optional[str] = None):
    """
    Configure LogLama to log to a SQLite database.

    Args:
        db_path: Path to the SQLite database file.
        table_name: Optional table name to use for logging. If not provided, a default name will be used.
    """
    # Ensure the directory exists
    db_dir = os.path.dirname(os.path.abspath(db_path))
    os.makedirs(db_dir, exist_ok=True)

    # Set environment variables for database logging
    os.environ["LOGLAMA_DB_LOGGING"] = "true"
    os.environ["LOGLAMA_DB_PATH"] = db_path

    if table_name:
        os.environ["LOGLAMA_DB_TABLE"] = table_name

    # Re-initialize logging with the new configuration
    setup_logging()

    # Add database info to global context
    set_global_context(db_path=db_path)


def configure_web_logging(host: str = "127.0.0.1", port: int = 8081):
    """
    Configure LogLama for web interface access.

    Args:
        host: Host to bind the web interface to.
        port: Port to bind the web interface to.
    """
    # Set environment variables for web interface
    os.environ["LOGLAMA_WEB_HOST"] = host
    os.environ["LOGLAMA_WEB_PORT"] = str(port)

    # Add web info to global context
    set_global_context(web_host=host, web_port=port)

    # Return the web URL for convenience
    return f"http://{host}:{port}"
