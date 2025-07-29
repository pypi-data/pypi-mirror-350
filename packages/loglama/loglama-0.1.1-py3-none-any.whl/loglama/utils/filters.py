#!/usr/bin/env python3
"""
Filters for LogLama.

This module provides filters that can be used to filter log records based on various criteria.
"""

import logging
import re
from typing import Any, Dict, List, Optional, Pattern, Union

from loglama.utils.context import LogContext


class LevelFilter(logging.Filter):
    """Filter that allows log records within a specific level range."""

    def __init__(
        self, min_level: Optional[int] = None, max_level: Optional[int] = None
    ):
        """Initialize the filter with the specified level range.

        Args:
            min_level: Minimum log level to allow (default: None, no minimum)
            max_level: Maximum log level to allow (default: None, no maximum)
        """
        super().__init__()
        self.min_level = min_level
        self.max_level = max_level

    def filter(self, record):
        """Filter the log record based on its level.

        Returns:
            True if the record should be logged, False otherwise
        """
        # Check if the record level is within the specified range
        if self.min_level is not None and record.levelno < self.min_level:
            return False
        if self.max_level is not None and record.levelno > self.max_level:
            return False
        return True


class ModuleFilter(logging.Filter):
    """Filter that allows log records from specific modules."""

    def __init__(
        self,
        include_modules: Optional[List[str]] = None,
        exclude_modules: Optional[List[str]] = None,
    ):
        """Initialize the filter with the specified module lists.

        Args:
            include_modules: List of module names to include (default: None, include all)
            exclude_modules: List of module names to exclude (default: None, exclude none)
        """
        super().__init__()
        self.include_modules = include_modules
        self.exclude_modules = exclude_modules

    def filter(self, record):
        """Filter the log record based on its module.

        Returns:
            True if the record should be logged, False otherwise
        """
        # Check if the record module is in the exclude list
        if self.exclude_modules is not None:
            for module in self.exclude_modules:
                if record.name.startswith(module):
                    return False

        # Check if the record module is in the include list
        if self.include_modules is not None:
            for module in self.include_modules:
                if record.name.startswith(module):
                    return True
            return False

        return True


class ContextFilter(logging.Filter):
    """Filter that adds context information to log records and can filter based on context values."""

    def __init__(
        self,
        include_context: Optional[Dict[str, Any]] = None,
        exclude_context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the filter with the specified context criteria.

        Args:
            include_context: Dictionary of context key-value pairs to include (default: None, include all)
            exclude_context: Dictionary of context key-value pairs to exclude (default: None, exclude none)
        """
        super().__init__()
        self.include_context = include_context
        self.exclude_context = exclude_context

    def filter(self, record):
        """Filter the log record based on its context and add context information to the record.

        Returns:
            True if the record should be logged, False otherwise
        """
        # Get the current context
        context = LogContext.get_context()

        # Add the context to the record
        record.context = context

        # Check if the record context matches the exclude criteria
        if self.exclude_context is not None:
            for key, value in self.exclude_context.items():
                if key in context and context[key] == value:
                    return False

        # Check if the record context matches the include criteria
        if self.include_context is not None:
            for key, value in self.include_context.items():
                if key not in context or context[key] != value:
                    return False

        return True


class RegexFilter(logging.Filter):
    """Filter that allows log records that match a regular expression pattern."""

    def __init__(self, pattern: Union[str, Pattern], field: str = "message"):
        """Initialize the filter with the specified pattern and field.

        Args:
            pattern: Regular expression pattern to match
            field: Record attribute to match against (default: "message")
        """
        super().__init__()
        self.pattern = (
            re.compile(pattern) if isinstance(pattern, str) else pattern
        )
        self.field = field

    def filter(self, record):
        """Filter the log record based on whether it matches the pattern.

        Returns:
            True if the record should be logged, False otherwise
        """
        # Get the value to match against
        if self.field == "message":
            value = record.getMessage()
        else:
            value = getattr(record, self.field, "")

        # Check if the value matches the pattern
        return bool(self.pattern.search(str(value)))
