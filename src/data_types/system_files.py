from dataclasses import dataclass
from re import findall


@dataclass
class DirectoryFile:
    """data structure"""

    name: str
    path: str

    def get_chapter_number_from_file(self) -> int:
        """function to get chapter number out of file name"""
        return int(findall("[0-9]+", self.name)[0])
