"""
Handles low-level operations related to the note repository file, such as 
creating, reading, and writing JSON data.

This module abstracts interactions with the file system to manage the 
repository where notes are stored.
"""
import json
from pathlib import Path

from app.core import REPOSITORY_FILENAME, REPOSITORY_TEMPLATE
from app.core.errors import RepositoryDoesNotExistError, RepositoryCorruptedError

repository = Path() / REPOSITORY_FILENAME

def create_repository():
    """
    Creates a new note repository file in the current directory.

    Raises:
        FileExistsError: If the repository file already exists.

    Returns:
        Path: Absolute path to the newly created repository file.
    """
    try:
        with repository.open("x") as file:
            json.dump(REPOSITORY_TEMPLATE, file)
            return repository.absolute()
    except FileExistsError:
        raise FileExistsError(f"Notes repository already initialized in {repository.absolute()}")

def load_repository():
    """
    Loads notes from the repository file as a dictionary.

    Raises:
        RepositoryDoesNotExistError: If the repository file does not exist.
        RepositoryCorruptedError: If the repository file is not valid JSON.

    Returns:
        dict: Parsed repository content as a dictionary of notes.
    """
    if not repository.exists():
        raise RepositoryDoesNotExistError(f"Notes repository does not exist. Run `note init` to initialize repository.")
    
    try:
        with open(REPOSITORY_FILENAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        raise RepositoryCorruptedError(f"Cannot read repository. File is not valid JSON. {error}")

def save_repository(notes_repository: dict):
    """
    Saves the provided repository dictionary to the repository file.

    Args:
        notes_repository (dict): The repository data to save.

    Raises:
        RepositoryDoesNotExistError: If the repository file does not exist.
    """
    if not repository.exists():
        raise RepositoryDoesNotExistError(f"Notes repository does not exist. Run `note init` to initialize repository.")
    
    with repository.open("w") as file:
        json.dump(notes_repository, file)

# TODO Consider using with clause to work with load/save repository