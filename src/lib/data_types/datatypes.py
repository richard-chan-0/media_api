from dataclasses import dataclass


@dataclass
class VideoRequest:
    source: str
    volume_number: int
    start_number: int = 0
