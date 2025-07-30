"""
Add command for the note application.

This module defines the `add` command which saves note to repository.
"""
import typer
from typing_extensions import Annotated

from app.core.models import Note
from app.core.repository import add_note
from app.core.errors import NoteAppError
from app.core.utils import parse_tags

app = typer.Typer()

@app.command()
def add(
    content: Annotated[
        str,
        typer.Argument(
            help="Content of the note."
        )
    ],
    tags: Annotated[
        str | None, 
        typer.Option(
            "--tags", 
            "-t", 
            help="Tags to be added to the note. Should be a string of comma" \
            " separated values with no white characters between."
        )
    ] = None
):
    """
    Add a new note with specified CONTENT and optional TAGS.

    TAGS should be a string of comma separated values associated to the
    note (e.g. "personal,todo"). 
    """

    try:
        tags_list = parse_tags(tags) if tags is not None else None    
        note = Note.create(content, tags_list)
        add_note(note)
    except NoteAppError as error:
        print(error)