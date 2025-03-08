from dataclasses import dataclass


@dataclass
class VideoRequest:
    source: str
    volume_number: int
    start_number: int = 0


@dataclass
class ComicRequest:
    source: str
    comic_name: str
