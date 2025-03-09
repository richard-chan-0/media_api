from dataclasses import dataclass
from marshmallow_dataclass import class_schema


@dataclass
class VideoRequest:
    source: str
    season_number: int = 1
    start_number: int = 0


@dataclass
class ComicRequest:
    source: str
    comic_name: str
    start_number: int = 0


@dataclass
class NameChange:
    old_path: str
    new_path: str


@dataclass
class NameChangeRequest:
    changes: list[NameChange]


VideoRequestSchema = class_schema(VideoRequest)
video_request_schema = VideoRequestSchema()

ComicRequestSchema = class_schema(ComicRequest)
comic_request_schema = ComicRequestSchema()

NameChangeRequestSchema = class_schema(NameChangeRequest)
name_change_request_schema = NameChangeRequestSchema()
