# loglama/diagnostics/health.py

"""Health check functions for diagnosing LogLama issues."""

import json
import logging
import os
import sqlite3
import sys
import tempfile
import threading
from typing import Any, Dict, Optional

from ..core.logger import get_logger, setup_logging
from ..handlers.sqlite_handler import SQLiteHandler
from ..utils.context import LogContext

# Create a logger for the diagnostics module
diag_logger = get_logger("loglama.diagnostics")


def check_system_health() -> Dict[str, Any]:
    """Perform a comprehensive health check of the LogLama system.

    Returns:
        Dict[str, Any]: A dictionary containing health status of various components
    """
    health_report = {
        "status": "healthy",
        "components": {},
        "issues": [],
        "recommendations": [],
    }

    # Check Python environment
    python_info = {
        "version": sys.version,
        "platform": sys.platform,
        "executable": sys.executable,
        "path": sys.path,
    }
    health_report["components"]["python"] = python_info  # type: ignore[index,str]

    # Check logging setup
    logging_status = verify_logging_setup()
    health_report["components"]["logging"] = logging_status  # type: ignore[index,str]
    if not logging_status["status"]:
        health_report["status"] = "degraded"
        health_report["issues"].extend(logging_status["issues"])  # type: ignore[attr-defined,str]
        health_report["recommendations"].extend(  # type: ignore[attr-defined,str]
            logging_status["recommendations"]
        )

    # Check context handling
    context_status = diagnose_context_issues()
    health_report["components"]["context"] = context_status  # type: ignore[index,str]
    if not context_status["status"]:
        health_report["status"] = "degraded"
        health_report["issues"].extend(context_status["issues"])  # type: ignore[attr-defined,str]
        health_report["recommendations"].extend(  # type: ignore[attr-defined,str]
            context_status["recommendations"]
        )

    # Check database connectivity
    db_status = check_database_connection()
    health_report["components"]["database"] = db_status  # type: ignore[index,str]
    if not db_status["status"]:
        health_report["status"] = "degraded"
        health_report["issues"].extend(db_status["issues"])  # type: ignore[attr-defined,str]
        health_report["recommendations"].extend(db_status["recommendations"])  # type: ignore[attr-defined,str]

    # Check file permissions
    file_status = check_file_permissions()
    health_report["components"]["file_permissions"] = file_status  # type: ignore[index,str]
    if not file_status["status"]:
        health_report["status"] = "degraded"
        health_report["issues"].extend(file_status["issues"])  # type: ignore[attr-defined,str]
        health_report["recommendations"].extend(file_status["recommendations"])  # type: ignore[attr-defined,str]

    return health_report


def verify_logging_setup() -> Dict[str, Any]:
    """Verify that the logging setup is working correctly.

    Returns:
        Dict[str, Any]: Status of the logging setup
    """
    result = {"status": True, "issues": [], "recommendations": []}

    # Create a temporary directory for test logs
    temp_dir = tempfile.TemporaryDirectory()
    log_file = os.path.join(temp_dir.name, "test_logging.log")
    db_file = os.path.join(temp_dir.name, "test_logging.db")

    try:
        # Setup logging with all handlers
        logger = setup_logging(
            name="test_diagnostics",
            level="INFO",
            console=True,
            file=True,
            file_path=log_file,
            database=True,
            db_path=db_file,
            json=True,
            context_filter=True,
        )

        # Log a test message
        test_message = "Diagnostic test message"
        logger.info(test_message)

        # Check if the log file was created and contains the message
        if not os.path.exists(log_file):
            result["status"] = False
            result["issues"].append("Log file was not created")  # type: ignore[attr-defined]
            result["recommendations"].append("Check file permissions and path")  # type: ignore[attr-defined]
        else:
            with open(log_file, "r") as f:
                content = f.read()
                if test_message not in content:
                    result["status"] = False
                    result["issues"].append(  # type: ignore[attr-defined]
                        "Test message not found in log file"
                    )
                    result["recommendations"].append(  # type: ignore[attr-defined]
                        "Check file handler configuration"
                    )

        # Check if the database was created and contains the message
        if not os.path.exists(db_file):
            result["status"] = False
            result["issues"].append("Database file was not created")  # type: ignore[attr-defined]
            result["recommendations"].append(  # type: ignore[attr-defined]
                "Check database permissions and path"
            )
        else:
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM logs WHERE message = ?", (test_message,)
                )
                row = cursor.fetchone()
                if not row:
                    result["status"] = False
                    result["issues"].append(  # type: ignore[attr-defined]
                        "Test message not found in database"
                    )
                    result["recommendations"].append(  # type: ignore[attr-defined]
                        "Check SQLite handler configuration"
                    )
                conn.close()
            except Exception as e:
                result["status"] = False
                result["issues"].append(f"Database error: {str(e)}")  # type: ignore[attr-defined]
                result["recommendations"].append(  # type: ignore[attr-defined]
                    "Check database schema and configuration"
                )

    except Exception as e:
        result["status"] = False
        result["issues"].append(f"Logging setup error: {str(e)}")  # type: ignore[attr-defined]
        result["recommendations"].append("Check logging configuration")  # type: ignore[attr-defined]

    # Clean up
    temp_dir.cleanup()

    return result


def diagnose_context_issues() -> Dict[str, Any]:
    """Diagnose issues with context handling.

    Returns:
        Dict[str, Any]: Status of context handling
    """
    result = {"status": True, "issues": [], "recommendations": []}

    # Create a temporary directory for test logs
    temp_dir = tempfile.TemporaryDirectory()
    log_file = os.path.join(temp_dir.name, "test_context.log")
    db_file = os.path.join(temp_dir.name, "test_context.db")

    try:
        # Setup logging
        logger = setup_logging(
            name="test_context",
            level="INFO",
            console=True,
            file=True,
            file_path=log_file,
            database=True,
            db_path=db_file,
            json=True,
            context_filter=True,
        )

        # Test context with LogContext
        test_user = "test_user"
        test_request_id = "test_request_id"

        with LogContext(user=test_user, request_id=test_request_id):
            logger.info("Test context message")

        # Check if context was added to log file
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                content = f.read()
                if test_user not in content or test_request_id not in content:
                    result["status"] = False
                    result["issues"].append("Context not found in log file")  # type: ignore[attr-defined]
                    result["recommendations"].append(  # type: ignore[attr-defined]
                        "Check ContextFilter and JSONFormatter"
                    )

        # Check if context was added to database
        if os.path.exists(db_file):
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT context FROM logs WHERE message = ?",
                    ("Test context message",),
                )
                row = cursor.fetchone()
                if row:
                    context = json.loads(row[0])
                    if (
                        context.get("user") != test_user
                        or context.get("request_id") != test_request_id
                    ):
                        result["status"] = False
                        result["issues"].append(  # type: ignore[attr-defined]
                            "Context values incorrect in database"
                        )
                        result["recommendations"].append(  # type: ignore[attr-defined]
                            "Check SQLiteHandler context handling"
                        )
                else:
                    result["status"] = False
                    result["issues"].append(  # type: ignore[attr-defined]
                        "Context message not found in database"
                    )
                    result["recommendations"].append(  # type: ignore[attr-defined]
                        "Check SQLiteHandler emit method"
                    )
                conn.close()
            except Exception as e:
                result["status"] = False
                result["issues"].append(f"Database context error: {str(e)}")  # type: ignore[attr-defined]
                result["recommendations"].append(  # type: ignore[attr-defined]
                    "Check database schema and context handling"
                )

        # Test thread-local context
        def thread_function():
            with LogContext(thread_user="thread_test"):
                logger.info("Thread context test")

        thread = threading.Thread(target=thread_function)
        thread.start()
        thread.join()

        # Check if thread context was isolated
        if os.path.exists(db_file):
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT context FROM logs WHERE message = ?",
                    ("Thread context test",),
                )
                row = cursor.fetchone()
                if row:
                    context = json.loads(row[0])
                    if (
                        context.get("thread_user") != "thread_test"
                        or "user" in context
                    ):
                        result["status"] = False
                        result["issues"].append("Thread context not isolated")  # type: ignore[attr-defined]
                        result["recommendations"].append(  # type: ignore[attr-defined]
                            "Check thread-local storage implementation"
                        )
                conn.close()
            except Exception as e:
                result["status"] = False
                result["issues"].append(f"Thread context error: {str(e)}")  # type: ignore[attr-defined]
                result["recommendations"].append(  # type: ignore[attr-defined]
                    "Check thread-local context handling"
                )

    except Exception as e:
        result["status"] = False
        result["issues"].append(f"Context test error: {str(e)}")  # type: ignore[attr-defined]
        result["recommendations"].append(  # type: ignore[attr-defined]
            "Check context handling implementation"
        )

    # Clean up
    temp_dir.cleanup()

    return result


def check_database_connection(db_path: Optional[str] = None) -> Dict[str, Any]:
    """Check database connection and schema.

    Args:
        db_path: Optional path to an existing database file

    Returns:
        Dict[str, Any]: Status of database connection
    """
    result = {"status": True, "issues": [], "recommendations": []}

    # If no db_path provided, create a temporary one
    temp_dir = None
    if not db_path:
        temp_dir = tempfile.TemporaryDirectory()
        db_path = os.path.join(temp_dir.name, "test_db.db")

    try:
        # Create a SQLiteHandler
        handler = SQLiteHandler(db_path)

        # Check if the database file exists
        if not os.path.exists(db_path):
            result["status"] = False
            result["issues"].append("Database file was not created")  # type: ignore[attr-defined]
            result["recommendations"].append(  # type: ignore[attr-defined]
                "Check database permissions and path"
            )
            return result

        # Check database schema
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if logs table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='logs'"
        )
        if not cursor.fetchone():
            result["status"] = False
            result["issues"].append("Logs table not found in database")  # type: ignore[attr-defined]
            result["recommendations"].append(  # type: ignore[attr-defined]
                "Check SQLiteHandler initialization"
            )
        else:
            # Check table schema
            cursor.execute("PRAGMA table_info(logs)")
            columns = {row[1] for row in cursor.fetchall()}
            required_columns = {
                "id",
                "timestamp",
                "level",
                "level_no",
                "logger_name",
                "message",
                "file_path",
                "line_number",
                "function",
                "module",
                "process",
                "process_name",
                "thread",
                "thread_name",
                "context",
                "extra",
            }

            missing_columns = required_columns - columns
            if missing_columns:
                result["status"] = False
                result["issues"].append(  # type: ignore[attr-defined]
                    f"Missing columns in logs table: {missing_columns}"
                )
                result["recommendations"].append(  # type: ignore[attr-defined]
                    "Check SQLiteHandler create_table method"
                )

        # Test a simple insert
        try:
            record = logging.LogRecord(
                name="test",
                level=logging.INFO,
                pathname="test.py",
                lineno=1,
                msg="Test database message",
                args=(),
                exc_info=None,
            )
            setattr(record, "context", {"test": "value"})

            handler.emit(record)

            # Verify the record was inserted
            cursor.execute(
                "SELECT * FROM logs WHERE message = ?",
                ("Test database message",),
            )
            if not cursor.fetchone():
                result["status"] = False
                result["issues"].append("Test record not inserted in database")  # type: ignore[attr-defined]
                result["recommendations"].append(  # type: ignore[attr-defined]
                    "Check SQLiteHandler emit method"
                )

        except Exception as e:
            result["status"] = False
            result["issues"].append(f"Database insert error: {str(e)}")  # type: ignore[attr-defined]
            result["recommendations"].append(  # type: ignore[attr-defined]
                "Check SQLiteHandler emit implementation"
            )

        conn.close()

    except Exception as e:
        result["status"] = False
        result["issues"].append(f"Database connection error: {str(e)}")  # type: ignore[attr-defined]
        result["recommendations"].append(  # type: ignore[attr-defined]
            "Check database configuration and permissions"
        )

    # Clean up if using temporary directory
    if temp_dir:
        temp_dir.cleanup()

    return result


def check_file_permissions(log_dir: Optional[str] = None) -> Dict[str, Any]:
    """Check file permissions for logging.

    Args:
        log_dir: Optional directory to check permissions

    Returns:
        Dict[str, Any]: Status of file permissions
    """
    result = {"status": True, "issues": [], "recommendations": []}

    # If no log_dir provided, create a temporary one
    temp_dir = None
    if not log_dir:
        temp_dir = tempfile.TemporaryDirectory()
        log_dir = temp_dir.name

    try:
        # Check if directory exists
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir, exist_ok=True)
            except Exception as e:
                result["status"] = False
                result["issues"].append(  # type: ignore[attr-defined]
                    f"Cannot create log directory: {str(e)}"
                )
                result["recommendations"].append(  # type: ignore[attr-defined]
                    "Check directory path and permissions"
                )
                return result

        # Check if directory is writable
        test_file_path = os.path.join(log_dir, "test_permissions.log")
        try:
            with open(test_file_path, "w") as f:
                f.write("Test write permissions")

            # Check if file was created
            if not os.path.exists(test_file_path):
                result["status"] = False
                result["issues"].append("Test file was not created")  # type: ignore[attr-defined]
                result["recommendations"].append("Check file permissions")  # type: ignore[attr-defined]
            else:
                # Clean up test file
                os.remove(test_file_path)

        except Exception as e:
            result["status"] = False
            result["issues"].append(f"File write error: {str(e)}")  # type: ignore[attr-defined]
            result["recommendations"].append(  # type: ignore[attr-defined]
                "Check file permissions and disk space"
            )

        # Check disk space
        try:
            stat = os.statvfs(log_dir)
            free_space = stat.f_frsize * stat.f_bavail
            if free_space < 10 * 1024 * 1024:  # Less than 10MB
                result["status"] = False
                result["issues"].append(  # type: ignore[attr-defined]
                    f"Low disk space: {free_space / (1024 * 1024):.2f} MB free"
                )
                result["recommendations"].append(  # type: ignore[attr-defined]
                    "Free up disk space or change log directory"
                )
        except Exception as e:
            result["status"] = False
            result["issues"].append(f"Disk space check error: {str(e)}")  # type: ignore[attr-defined]
            result["recommendations"].append("Check disk space manually")  # type: ignore[attr-defined]

    except Exception as e:
        result["status"] = False
        result["issues"].append(f"File permission check error: {str(e)}")  # type: ignore[attr-defined]
        result["recommendations"].append("Check file system permissions")  # type: ignore[attr-defined]

    # Clean up if using temporary directory
    if temp_dir:
        temp_dir.cleanup()

    return result
