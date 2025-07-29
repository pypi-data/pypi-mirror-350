#!/usr/bin/env python3
"""
Colored formatter for LogLama.

This module provides a formatter that outputs colored log records for better readability in the console.
"""

import logging
from typing import Dict, Optional

# Try to import colorama for cross-platform colored output
try:
    import colorama  # type: ignore[import-untyped]
    from colorama import Back, Fore, Style

    colorama.init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

    # Create dummy color constants
    class DummyColors:
        def __getattr__(self, name):
            return ""

    Fore = Back = Style = DummyColors()


class ColoredFormatter(logging.Formatter):
    """Formatter that outputs colored log records for better readability in the console."""

    # Default colors for different log levels
    LEVEL_COLORS = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Style.BRIGHT,
    }

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        level_colors: Optional[Dict[str, str]] = None,
    ):
        """Initialize the formatter with the specified format and date format.

        Args:
            fmt: Log format string (default: None)
            datefmt: Date format string (default: None)
            level_colors: Dictionary mapping log levels to colors (default: None)
        """
        if fmt is None:
            fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        super().__init__(fmt=fmt, datefmt=datefmt)

        # Use custom level colors if provided, otherwise use defaults
        self.level_colors = level_colors or self.LEVEL_COLORS

    def format(self, record) -> str:
        """Format the log record with colors."""
        # Skip coloring if colorama is not available
        if not COLORAMA_AVAILABLE:
            return super().format(record)

        # Get the color for this log level
        level_color = self.level_colors.get(record.levelname, "")

        # Save the original levelname
        original_levelname = record.levelname

        # Add color to the level name
        record.levelname = f"{level_color}{record.levelname}{Style.RESET_ALL}"

        # Format the record
        formatted = super().format(record)

        # Restore the original levelname
        record.levelname = original_levelname

        return formatted
