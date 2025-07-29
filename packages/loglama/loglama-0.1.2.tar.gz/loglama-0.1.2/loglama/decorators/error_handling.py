"""Error handling decorators for LogLama.

This module provides decorators for enhanced error logging and handling.
"""

import functools
import inspect
import sys
import traceback
from datetime import datetime
from typing import Any, Callable, Optional, TypeVar, cast

from loglama.core.logger import get_logger
from loglama.utils.context import LogContext

# Type for decorated functions
F = TypeVar("F", bound=Callable[..., Any])

# Get logger
logger = get_logger(__name__)


def log_errors(
    reraise: bool = True,
    log_level: str = "ERROR",
    include_traceback: bool = True,
    include_args: bool = True,
    max_arg_length: int = 1000,
    capture_locals: bool = False,
) -> Callable[[F], F]:
    """Decorator to log errors that occur in the decorated function.

    This decorator will catch any exceptions raised by the decorated function,
    log them with detailed context information, and optionally re-raise them.

    Args:
        reraise: Whether to re-raise the exception after logging
        log_level: The log level to use for error messages
        include_traceback: Whether to include the traceback in the log message
        include_args: Whether to include function arguments in the log message
        max_arg_length: Maximum length for argument values in the log message
        capture_locals: Whether to capture local variables in the log message

    Returns:
        Callable: Decorator function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get function signature and module
            sig = inspect.signature(func)
            module_name = func.__module__

            # Create context for this function call
            context = {
                "function": func.__name__,
                "module": module_name,
                "timestamp": datetime.now().isoformat(),
            }

            # Add arguments to context if requested
            if include_args:
                # Get parameter names
                param_names = list(sig.parameters.keys())

                # Add positional arguments
                for i, arg in enumerate(args):
                    arg_name = (
                        param_names[i] if i < len(param_names) else f"arg_{i}"
                    )
                    arg_value = str(arg)
                    if len(arg_value) > max_arg_length:
                        arg_value = arg_value[:max_arg_length] + "..."
                    context[arg_name] = arg_value

                # Add keyword arguments
                for key, value in kwargs.items():
                    arg_value = str(value)
                    if len(arg_value) > max_arg_length:
                        arg_value = arg_value[:max_arg_length] + "..."
                    context[key] = arg_value

            # Execute function with error logging context
            with LogContext(**context):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Get exception details
                    exc_type = type(e).__name__
                    exc_msg = str(e)
                    exc_traceback = (
                        traceback.format_exc() if include_traceback else None
                    )

                    # Add exception details to context
                    error_context = {
                        "error_type": exc_type,
                        "error_message": exc_msg,
                    }

                    if include_traceback:
                        error_context["traceback"] = exc_traceback  # type: ignore[assignment]

                    # Capture local variables if requested
                    if capture_locals:
                        frame = sys.exc_info()[2].tb_frame  # type: ignore[union-attr]
                        while frame:
                            if frame.f_code.co_name == func.__name__:
                                # Found the function frame
                                locals_dict = {}
                                for key, value in frame.f_locals.items():
                                    # Skip special variables and large objects
                                    if not key.startswith(
                                        "__"
                                    ) and not key.endswith("__"):
                                        try:
                                            value_str = str(value)
                                            if len(value_str) > max_arg_length:
                                                value_str = (
                                                    value_str[:max_arg_length]
                                                    + "..."
                                                )
                                            locals_dict[key] = value_str
                                        except Exception:
                                            locals_dict[key] = "<unprintable>"
                                error_context["locals"] = locals_dict  # type: ignore[str | Any,assignment, str]
                                break
                            frame = frame.f_back

                    # Log the error with context
                    with LogContext(**error_context):
                        log_method = getattr(
                            logger, log_level.lower(), logger.error
                        )
                        log_method(f"Error in {func.__name__}: {exc_msg}")

                    # Re-raise the exception if requested
                    if reraise:
                        raise

                    # Return None if not re-raising
                    return None

        return cast(F, wrapper)

    return decorator


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
    log_retries: bool = True,
) -> Callable[[F], F]:
    """Decorator to retry a function if it raises an exception.

    This decorator will retry the decorated function if it raises an exception,
    with an exponential backoff delay between retries.

    Args:
        max_attempts: Maximum number of attempts to make
        delay: Initial delay between retries in seconds
        backoff_factor: Factor to multiply delay by after each retry
        exceptions: Tuple of exceptions to catch and retry on
        log_retries: Whether to log retry attempts

    Returns:
        Callable: Decorator function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            import time

            # Get function name for logging
            func_name = func.__name__

            # Create context for this function call
            context = {
                "function": func_name,
                "retry_enabled": True,
                "max_attempts": max_attempts,
            }

            # Execute function with retry context
            with LogContext(**context):
                attempt = 1
                current_delay = delay

                while attempt <= max_attempts:
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        # Check if this is the last attempt
                        if attempt == max_attempts:
                            # Log the final failure
                            if log_retries:
                                logger.error(
                                    f"Failed all {max_attempts} attempts to execute {func_name}: {str(e)}"
                                )
                            raise

                        # Log the retry
                        if log_retries:
                            logger.warning(
                                f"Attempt {attempt}/{max_attempts} for {func_name} failed: {str(e)}. Retrying in {current_delay:.2f}s."  # noqa: E501
                            )

                        # Wait before retrying
                        time.sleep(current_delay)

                        # Increase the delay for the next retry
                        current_delay *= backoff_factor

                        # Increment the attempt counter
                        attempt += 1

        return cast(F, wrapper)

    return decorator


def fallback(
    default_value: Any = None,
    log_failures: bool = True,
    log_level: str = "WARNING",
) -> Callable[[F], F]:
    """Decorator to provide a fallback value if the function raises an exception.

    This decorator will catch any exceptions raised by the decorated function
    and return a default value instead.

    Args:
        default_value: Value to return if the function raises an exception
        log_failures: Whether to log failures
        log_level: The log level to use for failure messages

    Returns:
        Callable: Decorator function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get function name for logging
            func_name = func.__name__

            # Create context for this function call
            context = {"function": func_name, "fallback_enabled": True}

            # Execute function with fallback context
            with LogContext(**context):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Log the failure
                    if log_failures:
                        log_method = getattr(
                            logger, log_level.lower(), logger.warning
                        )
                        log_method(
                            f"Function {func_name} failed, using fallback value: {str(e)}"
                        )

                    # Return the default value
                    return default_value

        return cast(F, wrapper)

    return decorator


def timeout(
    seconds: float,
    fallback_value: Optional[Any] = None,
    log_timeouts: bool = True,
) -> Callable[[F], F]:
    """Decorator to apply a timeout to a function.

    This decorator will raise a TimeoutError if the function takes longer than
    the specified number of seconds to execute, or return a fallback value.

    Args:
        seconds: Maximum number of seconds the function can run
        fallback_value: Value to return if the function times out (if None, raises TimeoutError)
        log_timeouts: Whether to log timeouts

    Returns:
        Callable: Decorator function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            import signal

            # Get function name for logging
            func_name = func.__name__

            # Create context for this function call
            context = {"function": func_name, "timeout_seconds": seconds}

            # Define timeout handler
            def timeout_handler(signum: int, frame: Any) -> None:
                raise TimeoutError(
                    f"Function {func_name} timed out after {seconds} seconds"
                )

            # Execute function with timeout context
            with LogContext(**context):
                # Set up the timeout
                old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(int(seconds))

                try:
                    result = func(*args, **kwargs)
                    return result
                except TimeoutError as e:
                    # Log the timeout
                    if log_timeouts:
                        logger.warning(str(e))

                    # Raise or return fallback value
                    if fallback_value is None:
                        raise
                    return fallback_value
                finally:
                    # Reset the alarm and restore the old handler
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, old_handler)

        return cast(F, wrapper)

    return decorator
