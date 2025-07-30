"""
List command for the note application.

This module defines the `list` command, which displays notes from the current
repository. Notes can be optionally filtered by tags. If no filter is provided,
all notes in the repository are listed.
"""
import typer
from typing_extensions import Annotated

from app.core.errors import NoteAppError
from app.core.repository import list_notes, list_tags

app = typer.Typer()

@app.command()
def list(
    tag_filter: Annotated[
        list[str] | None,
        typer.Option(
            "--tag",
            "-t",
            help="List only notes with given tag. Can be used sequentially" \
            " to display notes that match any of given tags."
        )
    ] = None,
    tags_only: Annotated[
        bool,
        typer.Option(
            "--tags-only",
            "-T",
            help="List all tags present in notes repository."
        )
    ] = False
):
    """
    List notes stored in the repository.

    If no filter is provided, all notes will be displayed. Use the `--tag` option
    to filter notes by one or more tags. Only notes that have at least one of the 
    specified tags will be shown.
    """
    try:
        if not tags_only:
            # TODO keep original id when listing with filter
            list_notes(tag_filter)
        else:
            list_tags()
    except NoteAppError as error:
        print(error)
