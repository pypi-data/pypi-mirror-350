#!/usr/bin/env python3
"""
API server for LogLama.

This module provides a Flask-based API server for accessing and managing logs.
"""

import json
from datetime import datetime
from typing import Optional

from flask import Flask, jsonify, request
from sqlalchemy import desc

# Import LogLama modules
from loglama.config.env_loader import get_env, load_env
from loglama.core.logger import get_logger
import logging
import sys

# Ensure environment variables are loaded
load_env(verbose=False)

# Get API configuration from environment variables
API_HOST = get_env("LOGLAMA_API_HOST", "127.0.0.1")
API_PORT = get_env("LOGLAMA_API_PORT", 9090, as_type=int)
API_DEBUG = get_env("LOGLAMA_API_DEBUG", False, as_type=bool)

# Set up logger
logger = get_logger("loglama.api")


def create_app():
    """Create and configure the Flask application."""
    # Create Flask app
    app = Flask(__name__)

    # Import database modules
    try:
        from loglama.db.models import LogRecord, create_tables, get_session

        # Ensure database tables exist
        create_tables()
    except ImportError:
        logger.warning(
            "Database module not available. Install loglama[db] for database support."
        )

        # Create dummy classes for type checking
        class DummyLogRecord:
            pass

        def dummy_get_session():
            return None

        def dummy_create_tables():
            pass

        LogRecord = DummyLogRecord
        get_session = dummy_get_session
        create_tables = dummy_create_tables

    # Define API routes

    @app.route("/api/logs", methods=["GET"])
    def get_logs():
        """Get log records with optional filtering."""
        try:
            # Check if database is available
            if "loglama.db.models" not in sys.modules:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Database module not available. Install loglama[db] for database support.",
                        }
                    ),
                    500,
                )

            # Get query parameters
            level = request.args.get("level")
            logger_name = request.args.get("logger")
            module = request.args.get("module")
            limit = request.args.get("limit", 100, type=int)
            offset = request.args.get("offset", 0, type=int)

            # Create session and query
            session = get_session()
            query = session.query(LogRecord)

            # Apply filters
            if level:
                query = query.filter(LogRecord.level == level.upper())
            if logger_name:
                query = query.filter(
                    LogRecord.logger_name.like(f"%{logger_name}%")
                )
            if module:
                query = query.filter(LogRecord.module.like(f"%{module}%"))

            # Get total count
            total_count = query.count()

            # Apply pagination and ordering
            query = (
                query.order_by(desc(LogRecord.timestamp))
                .limit(limit)
                .offset(offset)
            )

            # Execute query
            log_records = query.all()

            # Convert to JSON-serializable format
            results = [record.to_dict() for record in log_records]

            # Close session
            session.close()

            return jsonify(
                {
                    "status": "success",
                    "total": total_count,
                    "offset": offset,
                    "limit": limit,
                    "logs": results,
                }
            )
        except Exception as e:
            logger.exception(f"Error getting logs: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/logs/<int:log_id>", methods=["GET"])
    def get_log(log_id):
        """Get a specific log record by ID."""
        try:
            # Check if database is available
            if "loglama.db.models" not in sys.modules:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Database module not available. Install loglama[db] for database support.",
                        }
                    ),
                    500,
                )

            # Create session and query
            session = get_session()
            record = (
                session.query(LogRecord).filter(LogRecord.id == log_id).first()
            )

            if not record:
                session.close()
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": f"Log record with ID {log_id} not found",
                        }
                    ),
                    404,
                )

            # Convert to JSON-serializable format
            result = record.to_dict()

            # Close session
            session.close()

            return jsonify({"status": "success", "log": result})
        except Exception as e:
            logger.exception(f"Error getting log record: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/logs", methods=["POST"])
    def add_log():
        """Add a new log record."""
        try:
            # Check if database is available
            if "loglama.db.models" not in sys.modules:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Database module not available. Install loglama[db] for database support.",
                        }
                    ),
                    500,
                )

            # Get request data
            data = request.json

            # Validate required fields
            required_fields = ["level", "message"]
            for field in required_fields:
                if field not in data:
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": f"Missing required field: {field}",
                            }
                        ),
                        400,
                    )

            # Create log record
            record = LogRecord(
                timestamp=datetime.utcnow(),
                logger_name=data.get("logger_name", "external"),
                level=data["level"].upper(),
                level_number=logging.getLevelName(data["level"].upper()),
                message=data["message"],
                module=data.get("module", "external"),
                function=data.get("function", "external"),
                line_number=data.get("line_number", 0),
                process_id=data.get("process_id", 0),
                process_name=data.get("process_name", "external"),
                thread_id=data.get("thread_id", 0),
                thread_name=data.get("thread_name", "external"),
                exception_info=data.get("exception_info"),
                context=(
                    json.dumps(data.get("context", {}))
                    if data.get("context")
                    else None
                ),
            )

            # Save to database
            session = get_session()
            session.add(record)
            session.commit()

            # Get the ID of the new record
            log_id = record.id

            # Close session
            session.close()

            return jsonify(
                {
                    "status": "success",
                    "message": "Log record added successfully",
                    "log_id": log_id,
                }
            )
        except Exception as e:
            logger.exception(f"Error adding log record: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/logs/clear", methods=["POST"])
    def clear_logs():
        """Clear all log records or those matching specific criteria."""
        try:
            # Check if database is available
            if "loglama.db.models" not in sys.modules:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Database module not available. Install loglama[db] for database support.",
                        }
                    ),
                    500,
                )

            # Get request data
            data = request.json or {}

            # Create session and query
            session = get_session()
            query = session.query(LogRecord)

            # Apply filters
            if "level" in data:
                query = query.filter(LogRecord.level == data["level"].upper())
            if "logger_name" in data:
                query = query.filter(
                    LogRecord.logger_name.like(f"%{data['logger_name']}%")
                )
            if "module" in data:
                query = query.filter(
                    LogRecord.module.like(f"%{data['module']}%")
                )

            # Get count before deletion
            count = query.count()

            # Delete matching records
            query.delete()
            session.commit()

            # Close session
            session.close()

            return jsonify(
                {
                    "status": "success",
                    "message": f"Deleted {count} log records",
                }
            )
        except Exception as e:
            logger.exception(f"Error clearing logs: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/stats", methods=["GET"])
    def get_stats():
        """Get statistics about log records."""
        try:
            # Check if database is available
            if "loglama.db.models" not in sys.modules:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Database module not available. Install loglama[db] for database support.",
                        }
                    ),
                    500,
                )

            # Create session
            session = get_session()

            # Get total count
            total_count = session.query(LogRecord).count()

            # Get counts by level
            level_counts = {}
            for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
                count = (
                    session.query(LogRecord)
                    .filter(LogRecord.level == level)
                    .count()
                )
                level_counts[level] = count

            # Get counts by logger
            logger_counts = {}
            loggers = session.query(LogRecord.logger_name).distinct().all()
            for (logger_name,) in loggers:
                count = (
                    session.query(LogRecord)
                    .filter(LogRecord.logger_name == logger_name)
                    .count()
                )
                logger_counts[logger_name] = count

            # Close session
            session.close()

            return jsonify(
                {
                    "status": "success",
                    "total": total_count,
                    "by_level": level_counts,
                    "by_logger": logger_counts,
                }
            )
        except Exception as e:
            logger.exception(f"Error getting stats: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify(
            {
                "status": "success",
                "message": "LogLama API is running",
                "timestamp": datetime.utcnow().isoformat(),
                "version": get_version(),
            }
        )

    def get_version():
        """Get the LogLama version."""
        try:
            from loglama import __version__

            return __version__
        except ImportError:
            return "unknown"

    return app


def start_server(
    host: Optional[str] = None,
    port: Optional[int] = None,
    debug: Optional[bool] = None,
):
    """Start the API server."""
    # Use environment variables if parameters are not provided
    host = host or API_HOST
    port = port or API_PORT
    debug = debug if debug is not None else API_DEBUG

    # Create the app
    app = create_app()

    # Log server start
    logger.info(
        f"Starting LogLama API server on {host}:{port} (debug={debug})"
    )

    # Start the server
    app.run(host=host, port=port, debug=debug)

    return app

# Add missing import
