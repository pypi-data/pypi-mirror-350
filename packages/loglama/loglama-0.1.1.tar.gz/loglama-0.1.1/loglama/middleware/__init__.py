"""Middleware for LogLama integration with web frameworks."""

try:
    __all__ = ["FlaskLoggingMiddleware"]
except ImportError:
    __all__ = []

try:
    __all__.append("FastAPILoggingMiddleware")
except ImportError:
    pass
