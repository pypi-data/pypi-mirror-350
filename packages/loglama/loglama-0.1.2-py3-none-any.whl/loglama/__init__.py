"""LogLama - Powerful logging and debugging utility for PyLama ecosystem."""

__version__ = "0.1.0"

from loglama.config.env_loader import get_env, load_env
from loglama.core.logger import get_logger, setup_logging

# Provide convenient imports for users
__all__ = ["get_logger", "setup_logging", "load_env", "get_env"]
