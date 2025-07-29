#!/usr/bin/env python3
"""
Scheduled Log Collector for LogLama

This module provides functionality to periodically collect logs from various PyLama components
and import them into the central LogLama database.
"""

import argparse
import signal
import time
from typing import List, Optional

from loglama.collectors.log_collector import (
    collect_all_logs,
    collect_logs_from_component,
)
from loglama.config.env_loader import load_env

# Import LogLama components
from loglama.core.logger import get_logger

# Set up logger
logger = get_logger("loglama.collectors.scheduled_collector")

# Default collection interval in seconds
DEFAULT_INTERVAL = 300  # 5 minutes

# Flag to indicate whether the collector should continue running
running = True


def signal_handler(sig, frame):
    """
    Handle signals to gracefully stop the collector.

    Args:
        sig: Signal number
        frame: Current stack frame
    """
    global running
    logger.info(f"Received signal {sig}, stopping collector")
    running = False


def run_collector(
    components: Optional[List[str]] = None,
    interval: int = DEFAULT_INTERVAL,
    once: bool = False,
    verbose: bool = False,
):
    """
    Run the log collector periodically.

    Args:
        components: List of components to collect logs from (None for all)
        interval: Collection interval in seconds
        once: Run only once instead of periodically
        verbose: Show verbose output
    """
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Ensure environment variables are loaded
    load_env(verbose=verbose)

    # Log start
    if components:
        logger.info(
            f"Starting scheduled log collector for components: {', '.join(components)}"
        )
    else:
        logger.info("Starting scheduled log collector for all components")

    logger.info(f"Collection interval: {interval} seconds")

    # Run the collector
    global running  # noqa: F824
    while running:
        try:
            start_time = time.time()

            # Collect logs
            if components:
                # Collect logs from specified components
                total_count = 0
                for component in components:
                    count = collect_logs_from_component(component)
                    total_count += count
                    if verbose:
                        logger.info(f"Collected {count} logs from {component}")

                logger.info(
                    f"Collected {total_count} logs from specified components"
                )
            else:
                # Collect logs from all components
                results = collect_all_logs()
                total_count = sum(results.values())

                if verbose:
                    for component, count in results.items():
                        logger.info(f"Collected {count} logs from {component}")

                logger.info(
                    f"Collected {total_count} logs from all components"
                )

            # If only running once, break the loop
            if once:
                logger.info("Completed one-time collection, exiting")
                break

            # Calculate sleep time to maintain the interval
            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)

            if sleep_time > 0:
                logger.debug(
                    f"Sleeping for {sleep_time:.2f} seconds until next collection"
                )

                # Sleep in small increments to allow for graceful shutdown
                sleep_increment = 1.0  # 1 second
                slept = 0.0

                while running and slept < sleep_time:
                    time.sleep(min(sleep_increment, sleep_time - slept))
                    slept += sleep_increment

        except Exception as e:
            logger.exception(f"Error in scheduled log collector: {e}")
            # Sleep a bit before retrying to avoid rapid failure loops
            time.sleep(10)

    logger.info("Scheduled log collector stopped")


def main():
    """
    Main entry point for the scheduled log collector.
    """
    parser = argparse.ArgumentParser(
        description="Scheduled Log Collector for LogLama"
    )
    parser.add_argument(
        "--components",
        "-c",
        nargs="+",
        help="Components to collect logs from (default: all)",
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=int,
        default=DEFAULT_INTERVAL,
        help=f"Collection interval in seconds (default: {DEFAULT_INTERVAL})",
    )
    parser.add_argument(
        "--once",
        "-o",
        action="store_true",
        help="Run only once instead of periodically",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show verbose output"
    )

    args = parser.parse_args()

    # Run the collector
    run_collector(
        components=args.components,
        interval=args.interval,
        once=args.once,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
