"""Diagnostics decorators for LogLama.

This module provides decorators for running diagnostics on functions and methods.
"""

import functools
import inspect
import os
import time
from typing import Any, Callable, Optional, TypeVar, cast

from loglama.core.logger import get_logger
from loglama.diagnostics import check_system_health
from loglama.utils.context import LogContext
import traceback

# Type for decorated functions
F = TypeVar("F", bound=Callable[..., Any])

# Get logger
logger = get_logger(__name__)


def with_diagnostics(
    run_before: bool = True,
    run_after: bool = True,
    fix_issues: bool = True,
    log_results: bool = True,
) -> Callable[[F], F]:
    """Decorator to run diagnostics before and/or after function execution.

    This decorator will run diagnostic checks before and/or after the decorated
    function executes, and optionally attempt to fix any issues found.

    Args:
        run_before: Whether to run diagnostics before function execution
        run_after: Whether to run diagnostics after function execution
        fix_issues: Whether to attempt to fix issues found
        log_results: Whether to log diagnostic results

    Returns:
        Callable: Decorator function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get function signature and module
            sig = inspect.signature(func)  # noqa: F841
            module_name = func.__module__

            # Create context for this function call
            context = {
                "function": func.__name__,
                "module": module_name,
                "diagnostics_enabled": True,
            }

            # Execute function with diagnostics context
            with LogContext(**context):
                # Run pre-execution diagnostics if requested
                if run_before:
                    pre_result = check_system_health()

                    if log_results:
                        if pre_result["status"] == "healthy":
                            logger.info(
                                f"Pre-execution diagnostics for {func.__name__} passed"
                            )
                        else:
                            logger.warning(
                                f"Pre-execution diagnostics for {func.__name__} found {len(pre_result['issues'])} issues"  # noqa: E501
                            )
                            for issue in pre_result["issues"]:
                                logger.warning(f"Diagnostic issue: {issue}")

                    # Fix issues if requested and issues were found
                    if fix_issues and pre_result["issues"]:
                        from loglama.utils.auto_fix import apply_fixes

                        fix_results = apply_fixes(pre_result["issues"])

                        if log_results:
                            if fix_results["fixed"]:
                                logger.info(
                                    f"Fixed {len(fix_results['fixed'])} issues before executing {func.__name__}"
                                )
                            if fix_results["failed"]:
                                logger.warning(
                                    f"Failed to fix {len(fix_results['failed'])} issues before executing {func.__name__}"  # noqa: E501
                                )

                # Execute the function
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time

                # Add execution time to context
                with LogContext(execution_time=execution_time):
                    logger.debug(
                        f"Function {func.__name__} executed in {execution_time:.6f} seconds"
                    )

                # Run post-execution diagnostics if requested
                if run_after:
                    post_result = check_system_health()

                    if log_results:
                        if post_result["status"] == "healthy":
                            logger.info(
                                f"Post-execution diagnostics for {func.__name__} passed"
                            )
                        else:
                            logger.warning(
                                f"Post-execution diagnostics for {func.__name__} found {len(post_result['issues'])} issues"  # noqa: E501
                            )
                            for issue in post_result["issues"]:
                                logger.warning(f"Diagnostic issue: {issue}")

                    # Fix issues if requested and issues were found
                    if fix_issues and post_result["issues"]:
                        from loglama.utils.auto_fix import apply_fixes

                        fix_results = apply_fixes(post_result["issues"])

                        if log_results:
                            if fix_results["fixed"]:
                                logger.info(
                                    f"Fixed {len(fix_results['fixed'])} issues after executing {func.__name__}"
                                )
                            if fix_results["failed"]:
                                logger.warning(
                                    f"Failed to fix {len(fix_results['failed'])} issues after executing {func.__name__}"
                                )

                return result

        return cast(F, wrapper)

    return decorator


def monitor_performance(
    threshold_ms: float = 1000.0,
    log_level: str = "WARNING",
    include_args: bool = False,
) -> Callable[[F], F]:
    """Decorator to monitor the performance of a function.

    This decorator will measure the execution time of the decorated function
    and log a warning if it exceeds the specified threshold.

    Args:
        threshold_ms: Threshold in milliseconds for slow execution warning
        log_level: The log level to use for slow execution warnings
        include_args: Whether to include function arguments in the log message

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
                "performance_monitored": True,
                "threshold_ms": threshold_ms,
            }

            # Add arguments to context if requested
            if include_args:
                # Get parameter names
                param_names = list(sig.parameters.keys())

                # Add positional arguments
                for i, arg in enumerate(args):
                    if i < len(param_names):
                        arg_name = param_names[i]
                        try:
                            arg_str = str(arg)
                            if len(arg_str) > 100:
                                arg_str = arg_str[:100] + "..."
                            context[f"arg_{arg_name}"] = arg_str
                        except Exception:
                            context[f"arg_{arg_name}"] = "<unprintable>"

                # Add keyword arguments
                for key, value in kwargs.items():
                    try:
                        value_str = str(value)
                        if len(value_str) > 100:
                            value_str = value_str[:100] + "..."
                        context[f"kwarg_{key}"] = value_str
                    except Exception:
                        context[f"kwarg_{key}"] = "<unprintable>"

            # Execute function with performance monitoring context
            with LogContext(**context):
                # Measure execution time
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                execution_time_ms = execution_time * 1000.0

                # Log warning if execution time exceeds threshold
                if execution_time_ms > threshold_ms:
                    log_method = getattr(
                        logger, log_level.lower(), logger.warning
                    )
                    log_method(
                        f"Slow execution: {func.__name__} took {execution_time_ms:.2f}ms (threshold: {threshold_ms}ms)"
                    )
                else:
                    logger.debug(
                        f"Function {func.__name__} executed in {execution_time_ms:.2f}ms"
                    )

                return result

        return cast(F, wrapper)

    return decorator


def resource_usage_monitor(
    memory_threshold_mb: float = 100.0,
    cpu_threshold_percent: float = 90.0,
    log_level: str = "WARNING",
) -> Callable[[F], F]:
    """Decorator to monitor resource usage during function execution.

    This decorator will measure memory and CPU usage during the execution of
    the decorated function and log a warning if it exceeds the specified thresholds.

    Args:
        memory_threshold_mb: Threshold in MB for memory usage warning
        cpu_threshold_percent: Threshold in percent for CPU usage warning
        log_level: The log level to use for resource usage warnings

    Returns:
        Callable: Decorator function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Try to import psutil for resource monitoring
            try:
                import psutil  # type: ignore[import-untyped]

                psutil_available = True
            except ImportError:
                psutil_available = False
                logger.warning(
                    f"psutil not available, resource monitoring disabled for {func.__name__}"
                )

            # Get function name for logging
            func_name = func.__name__

            # Create context for this function call
            context = {
                "function": func_name,
                "resource_monitored": psutil_available,
            }

            # Execute function with resource monitoring context
            with LogContext(**context):
                if psutil_available:
                    # Get initial resource usage
                    process = psutil.Process(os.getpid())
                    initial_memory = process.memory_info().rss / (
                        1024 * 1024
                    )  # MB
                    initial_cpu_percent = process.cpu_percent(interval=0.1)

                    # Execute the function
                    result = func(*args, **kwargs)

                    # Get final resource usage
                    final_memory = process.memory_info().rss / (
                        1024 * 1024
                    )  # MB
                    final_cpu_percent = process.cpu_percent(interval=0.1)

                    # Calculate differences
                    memory_diff = final_memory - initial_memory
                    cpu_diff = (
                        final_cpu_percent - initial_cpu_percent
                        if final_cpu_percent > initial_cpu_percent
                        else 0
                    )

                    # Add resource usage to context
                    with LogContext(
                        memory_usage_mb=memory_diff, cpu_usage_percent=cpu_diff
                    ):
                        # Log warnings if thresholds are exceeded
                        log_method = getattr(
                            logger, log_level.lower(), logger.warning
                        )

                        if memory_diff > memory_threshold_mb:
                            log_method(
                                f"High memory usage: {func_name} used {memory_diff:.2f}MB (threshold: {memory_threshold_mb}MB)"  # noqa: E501
                            )

                        if cpu_diff > cpu_threshold_percent:
                            log_method(
                                f"High CPU usage: {func_name} used {cpu_diff:.2f}% CPU (threshold: {cpu_threshold_percent}%)"  # noqa: E501
                            )

                        # Log debug message with resource usage
                        logger.debug(
                            f"Function {func_name} used {memory_diff:.2f}MB memory and {cpu_diff:.2f}% CPU"
                        )

                    return result
                else:
                    # Execute the function without resource monitoring
                    return func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator


def diagnose_on_error(
    generate_report: bool = True,
    report_path: Optional[str] = None,
    fix_issues: bool = True,
) -> Callable[[F], F]:
    """Decorator to run diagnostics when an error occurs.

    This decorator will catch any exceptions raised by the decorated function,
    run diagnostic checks, and optionally generate a diagnostic report.

    Args:
        generate_report: Whether to generate a diagnostic report
        report_path: Path to save the diagnostic report (None for default)
        fix_issues: Whether to attempt to fix issues found

    Returns:
        Callable: Decorator function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get function name for logging
            func_name = func.__name__

            # Create context for this function call
            context = {
                "function": func_name,
                "error_diagnostics_enabled": True,
            }

            # Execute function with error diagnostics context
            with LogContext(**context):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Log the error
                    logger.error(f"Error in {func_name}: {str(e)}")

                    # Run diagnostics
                    from loglama.diagnostics import generate_diagnostic_report

                    report = generate_diagnostic_report()

                    # Log diagnostic results
                    if report["status"] == "healthy":
                        logger.info(
                            f"Diagnostics after error in {func_name} show no issues"
                        )
                    else:
                        logger.warning(
                            f"Diagnostics after error in {func_name} found {len(report['issues'])} issues"
                        )
                        for issue in report["issues"]:
                            logger.warning(f"Diagnostic issue: {issue}")

                    # Fix issues if requested and issues were found
                    if fix_issues and report["issues"]:
                        from loglama.utils.auto_fix import apply_fixes

                        fix_results = apply_fixes(report["issues"])

                        if fix_results["fixed"]:
                            logger.info(
                                f"Fixed {len(fix_results['fixed'])} issues after error in {func_name}"
                            )
                            # Try running the function again if fixes were applied
                            try:
                                logger.info(
                                    f"Retrying {func_name} after fixing issues"
                                )
                                return func(*args, **kwargs)
                            except Exception as retry_e:
                                logger.error(
                                    f"Retry of {func_name} failed after fixing issues: {str(retry_e)}"
                                )

                    # Generate report if requested
                    if generate_report:
                        import json
                        import tempfile
                        from datetime import datetime

                        # Add error details to report
                        report["error"] = {
                            "type": type(e).__name__,
                            "message": str(e),
                            "traceback": traceback.format_exc(),
                        }

                        # Generate report path if not provided
                        nonlocal report_path
                        if not report_path:
                            timestamp = datetime.now().strftime(
                                "%Y%m%d_%H%M%S"
                            )
                            report_path = os.path.join(
                                tempfile.gettempdir(),
                                f"loglama_error_report_{func_name}_{timestamp}.json",
                            )

                        # Save report to file
                        try:
                            with open(report_path, "w") as f:
                                json.dump(report, f, indent=2)
                            logger.info(
                                f"Diagnostic report saved to {report_path}"
                            )
                        except Exception as report_e:
                            logger.error(
                                f"Failed to save diagnostic report: {str(report_e)}"
                            )

                    # Re-raise the original exception
                    raise

        return cast(F, wrapper)

    return decorator
