#!/usr/bin/env python3
"""
Diagnostic commands for the LogLama CLI.

This module contains commands for troubleshooting LogLama issues
and diagnosing problems with the PyLama ecosystem.
"""

import json
import sys
from pathlib import Path

import click

from loglama.cli.utils import get_console
from loglama.core.env_manager import load_central_env
from loglama.core.logger import get_logger

# Get console instance
console = get_console()


@click.command()
@click.argument(
    "command",
    type=click.Choice(["system", "env", "logs", "deps", "all"]),
    default="all",
)
@click.option(
    "--output", default=None, help="Output file for diagnostic information"
)
@click.option("--log-dir", default=None, help="Directory containing log files")
@click.option("--db-path", default=None, help="Path to LogLama database")
@click.option(
    "--log-level", default="INFO", help="Log level for diagnostic output"
)
def diagnose(command, output, log_dir, db_path, log_level):
    """Run diagnostic tools to troubleshoot LogLama issues."""
    # Initialize CLI logger
    logger = get_logger("loglama.cli")

    try:
        # Load the central .env file
        load_central_env()

        # Import diagnostic modules
        try:
            from loglama.diagnostics.troubleshoot import run_diagnostics
        except ImportError:
            console.print("[red]Diagnostic module not available.[/red]")
            sys.exit(1)

        # Run diagnostics
        console.print(f"Running {command} diagnostics...")
        results = run_diagnostics(
            command=command,
            log_dir=log_dir,
            db_path=db_path,
            log_level=log_level,
        )

        # Output results
        if output:
            # Write results to file
            output_path = Path(output)
            with open(output_path, "w") as f:
                json.dump(results, f, indent=2, default=str)
            console.print(
                f"[green]Diagnostic results written to {output_path}[/green]"
            )
        else:
            # Print results to console
            console.print("\n[bold]Diagnostic Results:[/bold]")
            for section, section_results in results.items():
                console.print(f"\n[bold]{section.upper()}[/bold]")
                console.print("-" * 40)

                if isinstance(section_results, dict):
                    for key, value in section_results.items():
                        if isinstance(value, dict):
                            console.print(f"[bold]{key}:[/bold]")
                            for subkey, subvalue in value.items():
                                console.print(f"  {subkey}: {subvalue}")
                        else:
                            console.print(f"{key}: {value}")
                elif isinstance(section_results, list):
                    for item in section_results:
                        if isinstance(item, dict):
                            for key, value in item.items():
                                console.print(f"{key}: {value}")
                            console.print("")
                        else:
                            console.print(f"- {item}")
                else:
                    console.print(section_results)
    except Exception as e:
        logger.exception(f"Error running diagnostics: {str(e)}")
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@click.command()
def version():
    """Show LogLama version information."""
    try:
        # Get version information
        try:
            from loglama import __version__

            version_info = __version__
        except ImportError:
            version_info = "unknown"

        # Get package information
        try:
            import pkg_resources  # type: ignore[import-untyped]  # type: ignore[import-untyped]

            package_info = pkg_resources.get_distribution("loglama")
            location = package_info.location
            requires = package_info.requires
        except Exception:
            location = "unknown"
            requires = []

        # Print version information
        console.print(f"[bold]LogLama[/bold] version {version_info}")
        console.print(f"Installed at: {location}")

        if requires:
            console.print("\n[bold]Dependencies:[/bold]")
            for req in requires:
                console.print(f"- {req}")
    except Exception as e:
        console.print(
            f"[red]Error showing version information: {str(e)}[/red]"
        )
        sys.exit(1)
