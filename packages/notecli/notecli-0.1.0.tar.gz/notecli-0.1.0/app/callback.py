"""
Root-level CLI options and callbacks for the application.

This module defines the main callback function that handles global options
(e.g., --version) for the CLI. It is intended to be used as the top-level
callback for the Typer app, allowing global flags to be processed even when
no subcommand is provided.
"""

import typer

from app import __app_name__, __version__

def callback(
    version: bool = typer.Option(
        None,
        "--version",
        help="Show the application's version and exit.",
        is_eager=True
    )
):
    """
    CLI callback function for handling global options.

    Args:
        version (bool): If provided, prints the application version and exits 
                        immediately.

    This function is intended to be passed to `typer.Typer(callback=...)` and
    allows the app to respond to top-level flags like `--version`, even if no
    subcommand is given.
    """
    if version:
        print(f"{__app_name__} v{__version__}")
        raise typer.Exit()