#!/usr/bin/env python3
"""
Utility functions for the LogLama CLI.

This module provides shared utility functions for the CLI commands.
"""


# Try to import rich for enhanced console output
try:
    from rich.console import Console

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


# Simple console fallback if rich is not available
class SimpleConsole:
    def print(self, *args, **kwargs):
        # Strip basic rich formatting
        text = args[0] if args else ""
        # Remove color tags like [red], [green], etc.
        if isinstance(text, str):
            import re

            text = re.sub(r"\[([a-z/]+)\]", "", text)
        print(text)

    def log(self, *args, **kwargs):
        print(*args)


# Singleton console instance
_console = None


def get_console():
    """
    Get a console instance for output formatting.

    Returns:
        Console instance (rich.console.Console if available, SimpleConsole otherwise)
    """
    global _console

    if _console is None:
        if RICH_AVAILABLE:
            _console = Console()
        else:
            _console = SimpleConsole()

    return _console


def format_duration(seconds: float) -> str:
    """
    Format a duration in seconds to a human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.2f} μs"
    elif seconds < 1:
        return f"{seconds * 1_000:.2f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.2f}s"
    else:
        hours = int(seconds / 3600)
        remaining_seconds = seconds % 3600
        minutes = int(remaining_seconds / 60)
        remaining_seconds = remaining_seconds % 60
        return f"{hours}h {minutes}m {remaining_seconds:.2f}s"


def format_size(size_bytes: int) -> str:
    """
    Format a size in bytes to a human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
