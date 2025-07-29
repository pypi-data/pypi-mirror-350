#!/usr/bin/env python3

"""
LogLama Web Viewer CLI

This module provides a command-line interface for the LogLama web viewer.
"""

import os
import sys
from pathlib import Path

import click
from loglama.config.env_loader import get_env, load_env
from loglama.web.app import run_app

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@click.command()
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind to")
@click.option("--port", "-p", type=int, default=5000, help="Port to listen on")
@click.option("--db", "-d", help="Path to SQLite database file")
@click.option("--debug", is_flag=True, help="Enable debug mode")
def main(host, port, db, debug):
    """Run the LogLama web viewer."""
    # Load environment variables
    load_env(verbose=True)

    # Get database path from environment if not provided
    if not db:
        db = get_env("LOGLAMA_DB_PATH", None)
        if not db:
            log_dir = get_env("LOGLAMA_LOG_DIR", "./logs")
            db = os.path.join(log_dir, "loglama.db")

    # Ensure the database exists
    db_dir = os.path.dirname(db)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        click.echo(f"Created directory {db_dir}")

    if not os.path.exists(db):
        click.echo(f"Warning: Database file not found at {db}")
        click.echo("Creating an empty database file...")
        with open(db, "w") as f:  # noqa: F841
            pass

    click.echo(f"Starting LogLama web viewer on http://{host}:{port}")
    click.echo(f"Using database: {db}")

    # Run the web application
    run_app(host=host, port=port, db_path=db)


if __name__ == "__main__":
    main()
