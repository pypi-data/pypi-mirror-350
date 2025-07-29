#!/usr/bin/env python3
"""
Command-line interface for LogLama.

This module provides a CLI for interacting with the LogLama system and managing
the centralized environment for the entire PyLama ecosystem.
"""

import sys

import click

from loglama.cli.commands.diagnostic_commands import diagnose, version
from loglama.cli.commands.env_commands import env, init

# Import command modules
from loglama.cli.commands.logs_commands import (
    clear,
    collect,
    collect_daemon,
    logs,
    stats,
    view,
)
from loglama.cli.commands.project_commands import (
    check_deps,
    start,
    start_all,
    test,
)
from loglama.cli.commands.update_loggers import main as update_loggers

# Import CLI utilities
from loglama.cli.utils import get_console

# Import LogLama modules
from loglama.core.env_manager import load_central_env
from loglama.core.logger import get_logger

# Get console instance
console = get_console()

# Load environment variables from the central .env file
load_central_env()


@click.group()
def cli():
    """LogLama - Powerful logging and debugging utility for PyLama ecosystem."""


# Register commands

# Log management commands
cli.add_command(logs)
cli.add_command(view)
cli.add_command(clear)
cli.add_command(stats)
cli.add_command(collect)
cli.add_command(collect_daemon)

# Environment management commands
cli.add_command(init)
cli.add_command(env)

# Project management commands
cli.add_command(check_deps)
cli.add_command(test)
cli.add_command(start)
cli.add_command(start_all)

# Diagnostic commands
cli.add_command(diagnose)
cli.add_command(version)


# Update loggers command
@cli.command()  # type: ignore[no-redef]
@click.option(
    "--dry-run", is_flag=True, help="Don't actually update the database"
)
@click.option(
    "--all",
    is_flag=True,
    help="Process all logs, not just those with unknown logger names",
)
def update_loggers(dry_run, all):  # noqa: F811
    """Update logger names in the LogLama database.

    This command updates existing logs with better logger names based on the log message content.
    It helps fix logs with 'unknown' logger names by extracting component information from the messages.

    Use --all to process all logs, not just those with unknown logger names.
    """
    from loglama.cli.commands.update_loggers import main as update_loggers_main

    update_loggers_main(dry_run, all)


@click.command()
@click.option("--port", default=5000, help="Port to run the web interface on")
@click.option(
    "--host", default="127.0.0.1", help="Host to bind the web interface to"
)
@click.option("--db", default=None, help="Path to LogLama database")
@click.option("--debug/--no-debug", default=False, help="Run in debug mode")
@click.option(
    "--open/--no-open", default=True, help="Open browser after starting"
)
def web(port, host, db, debug, open):
    """Launch the web interface for viewing logs."""
    # Initialize CLI logger
    logger = get_logger("loglama.cli")

    try:
        # Import web interface module
        try:
            from loglama.web import create_app
        except ImportError:
            console.print(
                "[red]Web interface module not available. Install loglama[web] for web interface support.[/red]"
            )
            sys.exit(1)

        # Create and run the web application
        app = create_app(db_path=db)

        # Print startup message
        console.print(
            f"[green]Starting LogLama web interface at http://{host}:{port}/[/green]"
        )

        # Open browser if requested
        if open:
            import webbrowser

            webbrowser.open(f"http://{host}:{port}/")

        # Run the application
        app.run(host=host, port=port, debug=debug)
    except Exception as e:
        logger.exception(f"Error starting web interface: {str(e)}")
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


# Add web command
cli.add_command(web)


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        # Get logger for unhandled exceptions
        logger = get_logger("loglama.cli")
        logger.error(f"Unhandled exception in CLI: {str(e)}")
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__" or __name__ == "loglama.cli.main":
    main()
