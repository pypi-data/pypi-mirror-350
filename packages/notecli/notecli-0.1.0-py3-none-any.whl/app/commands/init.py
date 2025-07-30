"""
Initialization command for the note application.

This module defines the `init` command which prepares the environment
for storing notes. It typically creates a `.notes` file in the current 
directory.
"""
import typer

from app.core.repository import create_repository

app = typer.Typer()

@app.command()
def init():
    """
    Initialize empty notes repository in working directory.
    """
    try:
        repository = create_repository()
        print(f"Initialized empty notes repository in {repository}")
    except FileExistsError as error:
        print(error)
    