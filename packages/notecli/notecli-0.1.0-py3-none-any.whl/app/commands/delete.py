"""
Delete command for the note application.

This module defines the `delete` command which deletes note from repository.
"""
import typer
from typing_extensions import Annotated

from app.core.errors import NoteAppError
from app.core.repository import delete_note

app = typer.Typer()

@app.command()
def delete(
    id: Annotated[
        int,
        typer.Argument(
            help="ID of note to delete."
        )
    ]
):
    """
    Delete note with specified ID.
    """
    try:
        delete_note(id)
    except NoteAppError as error:
        print(error)