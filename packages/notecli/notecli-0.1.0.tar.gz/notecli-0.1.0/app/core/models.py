from dataclasses import dataclass, asdict

@dataclass
class Note:
    content: str
    tags: list[str] | None
    status: str | None

    @staticmethod
    def create(content: str, tags: list[str] | None = None, status: str | None = None):
        return Note(content, tags, status)

    def to_dict(self):
        return asdict(self)

@dataclass
class IndexedNote(Note):
    idx: int

@dataclass
class Status:
    name: str
    style: str
    priority: int

    @staticmethod
    def create(name: str, style: str | None, priority: int):
        style = style if style is not None else "white"
        return Status(name, style, priority)