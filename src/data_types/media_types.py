from dataclasses import dataclass
from abc import ABC


class MediaStream(ABC):
    pass


@dataclass
class AudioStream(MediaStream):
    steam_number: int
    language: str
    is_default: bool


@dataclass
class SubtitleStream(MediaStream):
    stream_number: int
    language: str
    is_default: bool
