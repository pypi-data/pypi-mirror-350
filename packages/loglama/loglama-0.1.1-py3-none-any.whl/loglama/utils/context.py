#!/usr/bin/env python3
"""
Context utilities for LogLama.

This module provides utilities for capturing and managing context information in logs.
"""

import threading
from typing import Any, Dict

# Thread-local storage for context data
_context_storage = threading.local()


class LogContext:
    """Context manager for adding context information to log records."""

    def __init__(self, **context):
        """Initialize the context manager with the specified context data.

        Args:
            **context: Context data to add to log records
        """
        self.context = context
        self.previous_context = None

    def __enter__(self):
        """Enter the context manager, saving the previous context and setting the new context."""
        # Save the previous context
        self.previous_context = getattr(_context_storage, "context", {})

        # Update the context with the new values
        new_context = self.previous_context.copy()
        new_context.update(self.context)
        _context_storage.context = new_context

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager, restoring the previous context."""
        # Restore the previous context
        _context_storage.context = self.previous_context

    @staticmethod
    def get_context() -> Dict[str, Any]:
        """Get the current context data.

        Returns:
            Dictionary containing the current context data
        """
        return getattr(_context_storage, "context", {}).copy()

    @staticmethod
    def set_context(context: Dict[str, Any]):
        """Set the current context data.

        Args:
            context: Dictionary containing the context data to set
        """
        _context_storage.context = context.copy()

    @staticmethod
    def clear_context():
        """Clear the current context data."""
        _context_storage.context = {}

    @staticmethod
    def update_context(**context):
        """Update the current context data with the specified values.

        Args:
            **context: Context data to add to the current context
        """
        current_context = getattr(_context_storage, "context", {})
        current_context.update(context)
        _context_storage.context = current_context


def capture_context_decorator(**context):
    """Decorator for adding context information to log records.

    This can be used to decorate functions to automatically add context information
    to all log records created within the function.

    Args:
        **context: Context data to add to log records

    Returns:
        Decorator function
    """

    def decorator(func):
        from functools import wraps

        @wraps(func)
        def wrapper(*args, **kwargs):
            with LogContext(**context):
                return func(*args, **kwargs)

        return wrapper

    return decorator


# For backward compatibility, alias the decorator to the same name as the context manager
# This allows @capture_context to work as a decorator
capture_context = capture_context_decorator
