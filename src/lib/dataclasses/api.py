from dataclasses import dataclass
from marshmallow_dataclass import class_schema


@dataclass
class VideoRequest:
    season_number: int
    source: str = ""
    start_number: int = 0


@dataclass
class ComicRequest:
    comic_name: str
    source: str = ""
    start_number: int = 0


@dataclass
class NameChange:
    old_path: str
    new_path: str


@dataclass
class NameChangeRequest:
    changes: list[NameChange]


NameChangeRequestSchema = class_schema(NameChangeRequest)
name_change_request_schema = NameChangeRequestSchema()
