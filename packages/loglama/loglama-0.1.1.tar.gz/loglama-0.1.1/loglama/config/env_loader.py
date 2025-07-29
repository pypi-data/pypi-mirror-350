#!/usr/bin/env python3
"""
Environment variable loader for LogLama.

This module provides functionality for loading environment variables from .env files
with robust error handling and multiple fallback locations.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Try to import dotenv for environment variable loading
try:
    from dotenv import load_dotenv as _load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

    def _load_dotenv(  # type: ignore[misc]
        dotenv_path=None, stream=None, verbose=False, override=False, **kwargs
    ):
        logging.warning(
            "python-dotenv package not found, environment variables from .env will not be loaded"
        )
        return False


# Set up basic logging for this module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)7s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Module logger
_logger = logging.getLogger(__name__)

# Environment variable cache
_env_cache: Dict[str, str] = {}

# Track if environment has been loaded
_env_loaded = False


def find_project_root(start_dir: Optional[Union[str, Path]] = None) -> Path:
    """
    Find the project root directory by looking for common project files.

    Args:
        start_dir: Directory to start the search from. If None, uses the current working directory.

    Returns:
        Path to the project root directory.
    """
    if start_dir is None:
        start_dir = Path.cwd()
    else:
        start_dir = Path(start_dir)

    # Convert to absolute path
    start_dir = start_dir.absolute()

    # List of files that indicate a project root
    root_indicators = [
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "requirements.txt",
        ".git",
        ".gitignore",
        "Makefile",
        "README.md",
    ]

    # Start from the current directory and go up
    current_dir = start_dir
    while current_dir != current_dir.parent:  # Stop at the root directory
        # Check if any of the indicator files exist in this directory
        for indicator in root_indicators:
            if (current_dir / indicator).exists():
                return current_dir

        # Move up one directory
        current_dir = current_dir.parent

    # If no project root found, return the starting directory
    _logger.warning(
        f"Could not find project root, using {start_dir} as fallback"
    )
    return start_dir


def get_env_file_paths(
    custom_path: Optional[Union[str, Path]] = None,
) -> List[Path]:
    """
    Get a list of potential .env file paths to try.

    Args:
        custom_path: Optional custom path to a .env file.

    Returns:
        List of potential .env file paths to try, in order of priority.
    """
    # Start with the custom path if provided
    env_paths = []
    if custom_path is not None:
        custom_path = Path(custom_path).expanduser().resolve()
        env_paths.append(custom_path)

    # Get the project root
    project_root = find_project_root()

    # Add standard locations
    env_paths.extend(
        [
            Path(os.getcwd()) / ".env",  # Current working directory
            project_root / ".env",  # Project root
            project_root / "config" / ".env",  # Project config directory
            project_root.parent / ".env",  # Parent directory (for monorepos)
            Path(os.path.expanduser("~")) / ".env",  # User's home directory
            Path(
                os.path.expanduser("~/.config/loglama/.env")
            ),  # User's config directory
        ]
    )

    # Remove duplicates while preserving order
    unique_paths = []
    for path in env_paths:
        if path not in unique_paths:
            unique_paths.append(path)

    return unique_paths


def load_env(
    env_file: Optional[Union[str, Path]] = None,
    override: bool = True,
    verbose: bool = True,
) -> bool:
    """
    Load environment variables from .env files with multiple fallback locations.

    This function will try to load environment variables from the specified .env file.
    If no file is specified, it will try several common locations.

    Args:
        env_file: Path to the .env file to load. If None, will try multiple locations.
        override: Whether to override existing environment variables.
        verbose: Whether to log information about the loading process.

    Returns:
        True if environment variables were loaded successfully, False otherwise.
    """
    global _env_loaded

    if not DOTENV_AVAILABLE and verbose:
        _logger.warning(
            "python-dotenv package not found. Install it with 'pip install python-dotenv' for .env file support."
        )
        return False

    # Get the list of .env file paths to try
    env_paths = get_env_file_paths(env_file)

    # Try to load from any available .env file
    env_loaded = False
    for env_path in env_paths:
        if env_path.exists():
            if verbose:
                _logger.info(f"Loading environment variables from {env_path}")

            # Load the .env file
            success = _load_dotenv(env_path, override=override)

            if success:
                env_loaded = True
                # Update the cache with the new values
                _update_env_cache()
                break

    if not env_loaded and verbose:
        _logger.warning(
            f"No .env file found in any of these locations: {[str(p) for p in env_paths]}"
        )
        _logger.info("Using default environment variables")

    # Mark as loaded even if no file was found
    _env_loaded = True

    return env_loaded


def _update_env_cache() -> None:
    """
    Update the environment variable cache with current environment variables.
    """
    global _env_cache
    _env_cache = dict(os.environ)


def get_env(
    key: str, default: Any = None, as_type: Optional[type] = None
) -> Any:
    """
    Get an environment variable with type conversion and default value.

    Args:
        key: The name of the environment variable.
        default: The default value to return if the environment variable is not set.
        as_type: The type to convert the environment variable to. If None, returns the string value.

    Returns:
        The environment variable value, converted to the specified type if provided.
    """
    # Load environment variables if not already loaded
    if not _env_loaded:
        load_env(verbose=False)

    # Get the value from the environment
    value = os.environ.get(key)

    # Return the default if the value is not set
    if value is None:
        return default

    # Return the value as is if no type conversion is requested
    if as_type is None:
        return value

    # Convert the value to the requested type
    try:
        if as_type is bool:
            # Special handling for boolean values
            return value.lower() in ("true", "1", "t", "yes", "y")
        elif as_type is list or as_type is List:
            # Special handling for list values
            return value.split(",") if value else []
        else:
            # Generic type conversion
            return as_type(value)
    except (ValueError, TypeError) as e:
        _logger.warning(
            f"Error converting environment variable {key}={value} to {as_type.__name__}: {e}"
        )
        return default


# Initialize the environment variable cache
_update_env_cache()
