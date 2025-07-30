import re

from rich import print
from rich.table import Table
from rich.text import Text

from app.core.errors import NoteAppError
from app.core.models import IndexedNote

DASH_TEXT = Text("-", style="italic black")

def parse_tags(tags: str):
    result = re.match("^[a-zA-Z0-9]+(,[a-zA-Z0-9]+)*$", tags)
    if result is None:
        raise NoteAppError("Note was not added because of an error. Tags " \
        "should be comma separated list of strings containing only " \
        "letters and numbers.") # TODO change to custom exception
    return tags.split(",")

def print_notes(notes: list[IndexedNote]):
    table = Table(title="Your Notes")
    table.add_column("ID", width=6)
    table.add_column("Content", width=60)
    table.add_column("Tags", style="violet", width=16)
    table.add_column("Status", width=16)

    for note in notes:
        idx, content, tags, status = note.idx, note.content, note.tags, note.status
        tags = " ".join(f"#{tag}" for tag in tags) if tags is not None else DASH_TEXT
        status = Text(status, style="green bold") if status is not None else DASH_TEXT
        table.add_row(str(idx + 1), content, tags, status)
    
    print(table)

def print_tags(tags: list[str]):
    tags_list = " ".join(f"#{tag}" for tag in tags)
    tags_list = Text(tags_list, style="bold violet")
    print(tags_list)
