class NoteAppError(Exception):
    """
    Base class for all custom exceptions in the note application.
    """
    pass

class RepositoryDoesNotExistError(NoteAppError):
    """
    Raised when a note repository is not found in the current directory.
    """
    pass

class RepositoryCorruptedError(NoteAppError):
    """
    Raised when a note repository cannot be loaded, likely due to invalid
    content (e.g. malformed JSON).
    """
    pass

class NotesNotFoundError(NoteAppError):
    """Raised when no notes are found in the repository, either because it 
    is empty or no notes match the filter."""
    pass