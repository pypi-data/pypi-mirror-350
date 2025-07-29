"""Auto-fix decorator for LogLama.

This module provides decorators for automatically detecting and fixing common issues.
"""

import functools
import inspect
import os
import sys
import traceback
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast  # noqa: F401

from loglama.core.logger import get_logger
from loglama.utils.context import LogContext

# Type for decorated functions
F = TypeVar('F', bound=Callable[..., Any])

# Get logger
logger = get_logger(__name__)

# Registry of known issues and their fixes
KNOWN_ISSUES = {
    "missing_file_permissions": "check_and_fix_file_permissions",
    "database_connection_error": "fix_database_connection",
    "invalid_log_level": "fix_log_level",
    "missing_environment_variable": "set_default_environment_variable",
    "circular_import": "detect_and_fix_circular_import",
    "thread_safety_issue": "apply_thread_safety_fix",
    "memory_leak": "fix_memory_leak",
    "file_handle_leak": "fix_file_handle_leak",
    "excessive_logging": "optimize_logging",
    "missing_context": "add_default_context",
}


def check_and_fix_file_permissions(path: str) -> bool:
    """Check and fix file permissions for log files.

    Args:
        path: Path to the file to check

    Returns:
        bool: True if fix was applied, False otherwise
    """
    if not os.path.exists(path):
        try:
            # Try to create the file
            with open(path, 'a'):
                pass
            logger.info(f"Created missing log file: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create log file: {path}, error: {str(e)}")
            return False

    # Check if file is writable
    if not os.access(path, os.W_OK):
        try:
            # Try to make the file writable
            os.chmod(path, 0o644)
            logger.info(f"Fixed permissions for log file: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to fix permissions for log file: {path}, error: {str(e)}")
            return False

    return False  # No fix needed


def fix_database_connection(db_path: str) -> bool:
    """Fix database connection issues.

    Args:
        db_path: Path to the database file

    Returns:
        bool: True if fix was applied, False otherwise
    """
    import sqlite3

    # Check if database directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"Created missing database directory: {db_dir}")
        except Exception as e:
            logger.error(f"Failed to create database directory: {db_dir}, error: {str(e)}")
            return False

    # Try to connect to the database
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
        logger.info(f"Verified database connection: {db_path}")
        return True
    except sqlite3.Error as e:  # noqa: F841
        # If database is corrupted, try to create a new one
        try:
            # Backup the corrupted database if it exists
            if os.path.exists(db_path):
                backup_path = f"{db_path}.backup"
                os.rename(db_path, backup_path)
                logger.warning(f"Backed up corrupted database to: {backup_path}")

            # Create a new database
            conn = sqlite3.connect(db_path)
            conn.close()
            logger.info(f"Created new database: {db_path}")
            return True
        except Exception as e2:
            logger.error(f"Failed to fix database: {db_path}, error: {str(e2)}")
            return False

    return False  # No fix needed


def fix_log_level(level: str) -> str:
    """Fix invalid log level by converting to a valid one.

    Args:
        level: The log level to fix

    Returns:
        str: The fixed log level
    """
    import logging

    valid_levels = {
        'CRITICAL': logging.CRITICAL,
        'FATAL': logging.FATAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'WARN': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET
    }

    # Convert to uppercase
    level_upper = level.upper() if isinstance(level, str) else str(level).upper()

    # If level is a valid level name, return it
    if level_upper in valid_levels:
        return level_upper

    # If level is a number, convert to corresponding level name
    try:
        level_num = int(level)
        for name, num in valid_levels.items():
            if level_num == num:
                logger.info(f"Converted numeric log level {level} to {name}")
                return name
    except (ValueError, TypeError):
        pass

    # Default to INFO if invalid
    logger.warning(f"Invalid log level '{level}', defaulting to 'INFO'")
    return 'INFO'


def set_default_environment_variable(var_name: str, default_value: str) -> bool:
    """Set a default environment variable if it's missing.

    Args:
        var_name: Name of the environment variable
        default_value: Default value to set

    Returns:
        bool: True if variable was set, False otherwise
    """
    if var_name not in os.environ:
        os.environ[var_name] = default_value
        logger.info(f"Set default environment variable {var_name}={default_value}")
        return True
    return False


def detect_and_fix_circular_import(module_name: str) -> bool:
    """Detect and fix circular import issues.

    Args:
        module_name: Name of the module to check

    Returns:
        bool: True if fix was applied, False otherwise
    """
    # This is a simplified implementation - in practice, this would be more complex
    # and would involve analyzing the import graph
    logger.warning(f"Circular import detection is limited. Please check module {module_name} manually.")
    return False


def apply_thread_safety_fix(obj: Any) -> bool:
    """Apply thread safety fixes to an object.

    Args:
        obj: Object to fix

    Returns:
        bool: True if fix was applied, False otherwise
    """
    # This is a simplified implementation - in practice, this would be more complex
    import threading

    # Check if object already has a lock attribute
    if not hasattr(obj, '_lock'):
        setattr(obj, '_lock', threading.RLock())
        logger.info(f"Added thread lock to {obj.__class__.__name__}")
        return True
    return False


def fix_memory_leak(obj: Any) -> bool:
    """Fix potential memory leaks.

    Args:
        obj: Object to check for memory leaks

    Returns:
        bool: True if fix was applied, False otherwise
    """
    # This is a simplified implementation - in practice, this would be more complex
    # and would involve analyzing object references and resource usage
    logger.warning(f"Memory leak detection is limited. Please check {obj.__class__.__name__} manually.")
    return False


def fix_file_handle_leak(file_obj: Any) -> bool:
    """Fix file handle leaks by ensuring files are properly closed.

    Args:
        file_obj: File object to check

    Returns:
        bool: True if fix was applied, False otherwise
    """
    if hasattr(file_obj, 'closed') and not file_obj.closed:
        try:
            file_obj.close()
            logger.info(f"Closed leaked file handle: {getattr(file_obj, 'name', 'unknown')}")
            return True
        except Exception as e:
            logger.error(f"Failed to close file handle: {str(e)}")
            return False
    return False


def optimize_logging(logger_name: str, threshold: int = 100) -> bool:
    """Optimize excessive logging by adjusting log levels.

    Args:
        logger_name: Name of the logger to optimize
        threshold: Threshold for number of log messages per second

    Returns:
        bool: True if optimization was applied, False otherwise
    """
    import logging

    # Get the logger
    log_obj = logging.getLogger(logger_name)

    # Check if logger is already optimized
    if hasattr(log_obj, '_optimized'):
        return False

    # Set a higher log level for DEBUG messages
    if log_obj.level <= logging.DEBUG:
        log_obj.setLevel(logging.INFO)
        setattr(log_obj, '_optimized', True)
        logger.info(f"Optimized logging for {logger_name} by raising log level to INFO")
        return True

    return False


def add_default_context(context_dict: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Add default context values if missing.

    Args:
        context_dict: Existing context dictionary or None

    Returns:
        Dict[str, Any]: Updated context dictionary
    """
    if context_dict is None:
        context_dict = {}

    # Add default context values if not present
    defaults = {
        'hostname': os.environ.get('HOSTNAME', 'unknown'),
        'pid': os.getpid(),
        'python_version': sys.version.split()[0],
    }

    for key, value in defaults.items():
        if key not in context_dict:
            context_dict[key] = value
            logger.debug(f"Added default context value: {key}={value}")

    return context_dict


def apply_fixes(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Apply fixes for detected issues.

    Args:
        issues: List of issues to fix

    Returns:
        Dict[str, Any]: Results of fix attempts
    """
    results = {  # type: ignore[var-annotated]
        'fixed': [],
        'failed': [],
        'ignored': []
    }

    for issue in issues:
        issue_type = issue.get('type')
        if issue_type in KNOWN_ISSUES:
            fix_func_name = KNOWN_ISSUES[issue_type]
            fix_func = globals().get(fix_func_name)

            if fix_func and callable(fix_func):
                try:
                    # Extract parameters for the fix function
                    params = issue.get('params', {})

                    # Apply the fix
                    success = fix_func(**params)

                    if success:
                        results['fixed'].append({
                            'type': issue_type,
                            'message': issue.get('message', 'No message provided')
                        })
                    else:
                        results['ignored'].append({
                            'type': issue_type,
                            'message': issue.get('message', 'No message provided'),
                            'reason': 'No fix needed or fix not applicable'
                        })
                except Exception as e:
                    results['failed'].append({
                        'type': issue_type,
                        'message': issue.get('message', 'No message provided'),
                        'error': str(e)
                    })
            else:
                results['failed'].append({
                    'type': issue_type,
                    'message': issue.get('message', 'No message provided'),
                    'error': f"Fix function '{fix_func_name}' not found"
                })
        else:
            results['ignored'].append({
                'type': issue_type,
                'message': issue.get('message', 'No message provided'),
                'reason': 'Unknown issue type'
            })

    return results


def auto_fix(func: F) -> F:
    """Decorator to automatically detect and fix common issues.

    This decorator will monitor the execution of the decorated function
    and attempt to automatically fix any detected issues.

    Args:
        func: Function to decorate

    Returns:
        F: Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Get function signature and module
        sig = inspect.signature(func)
        module_name = func.__module__

        # Create context for this function call
        context = {
            'function': func.__name__,
            'module': module_name,
            'auto_fix': True
        }

        # Add arguments to context if simple types
        for i, arg in enumerate(args):
            if isinstance(arg, (str, int, float, bool)):
                context[f'arg_{i}'] = arg

        for key, value in kwargs.items():
            if isinstance(value, (str, int, float, bool)):
                context[f'kwarg_{key}'] = value

        # Execute function with auto-fix context
        with LogContext(**context):
            try:
                # Check for common issues before execution
                pre_issues = []

                # Check file paths in arguments
                for param_name, param in sig.parameters.items():
                    if param_name in kwargs and isinstance(kwargs[param_name], str):
                        value = kwargs[param_name]
                        # Check if parameter looks like a file path
                        if os.path.sep in value and not os.path.isdir(value):
                            # Check file permissions if it exists
                            if os.path.exists(value) and not os.access(value, os.W_OK):
                                pre_issues.append({
                                    'type': 'missing_file_permissions',
                                    'message': f"File '{value}' is not writable",
                                    'params': {'path': value}
                                })
                            # Check if directory exists
                            dir_path = os.path.dirname(value)
                            if dir_path and not os.path.exists(dir_path):
                                try:
                                    os.makedirs(dir_path, exist_ok=True)
                                    logger.info(f"Created missing directory: {dir_path}")
                                except Exception as e:
                                    pre_issues.append({
                                        'type': 'missing_file_permissions',
                                        'message': f"Cannot create directory '{dir_path}': {str(e)}",
                                        'params': {'path': dir_path}
                                    })

                # Apply fixes for pre-execution issues
                if pre_issues:
                    pre_results = apply_fixes(pre_issues)
                    for fixed in pre_results['fixed']:
                        logger.info(f"Auto-fixed issue before execution: {fixed['message']}")

                # Execute the function
                result = func(*args, **kwargs)

                return result

            except Exception as e:
                # Detect issues based on the exception
                post_issues = []

                # Extract exception details
                exc_type = type(e).__name__
                exc_msg = str(e)
                exc_traceback = traceback.format_exc()

                # Check for specific exception types and add appropriate fixes
                if exc_type == 'PermissionError':
                    # Extract file path from exception message if possible
                    import re
                    path_match = re.search(r"'([^']+)'", exc_msg)
                    path = path_match.group(1) if path_match else None

                    if path:
                        post_issues.append({
                            'type': 'missing_file_permissions',
                            'message': f"Permission denied for file '{path}'",
                            'params': {'path': path}
                        })

                elif exc_type == 'sqlite3.OperationalError' and 'database is locked' in exc_msg:
                    # Extract database path from traceback if possible
                    import re
                    db_match = re.search(r"sqlite3\.connect\(['\"]([^'\"]+)['\"]\)", exc_traceback)
                    db_path = db_match.group(1) if db_match else None

                    if db_path:
                        post_issues.append({
                            'type': 'database_connection_error',
                            'message': f"Database is locked: '{db_path}'",
                            'params': {'db_path': db_path}
                        })

                elif exc_type == 'ValueError' and 'log level' in exc_msg.lower():
                    # Extract log level from exception message if possible
                    import re
                    level_match = re.search(r"Invalid log level[:\s]+[\"']?([^\"'\s]+)[\"']?", exc_msg, re.IGNORECASE)
                    level = level_match.group(1) if level_match else 'INFO'

                    post_issues.append({
                        'type': 'invalid_log_level',
                        'message': f"Invalid log level: '{level}'",
                        'params': {'level': level}
                    })

                # Apply fixes for post-execution issues
                if post_issues:
                    post_results = apply_fixes(post_issues)
                    for fixed in post_results['fixed']:
                        logger.info(f"Auto-fixed issue after exception: {fixed['message']}")

                    # If we fixed any issues, try to run the function again
                    if post_results['fixed']:
                        logger.info(f"Retrying function {func.__name__} after fixing issues")
                        return func(*args, **kwargs)

                # If we couldn't fix the issue, re-raise the exception
                raise

    return cast(F, wrapper)
