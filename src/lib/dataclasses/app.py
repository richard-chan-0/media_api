from dataclasses import dataclass
from re import findall, sub
from src.lib.exceptions.exceptions import DataTypeError
from typing import Callable


@dataclass
class DirectoryFile:
    """data structure"""

    name: str
    path: str

    def __get_first_number(self, text: str) -> str:
        """function to get the first instance of a number"""
        matches = findall("\d+", text)
        if not matches:
            raise DataTypeError("no numbers found in file name")
        return matches[0]

    def __get_season_episode_matches(self) -> str:
        return findall("S\d\dE\d+", self.name)[0]

    def __get_episode_matches(self) -> str:
        clean_resolution_text = sub("(720|1080|360|1920|1440)", "?", self.name)
        return self.__get_first_number(clean_resolution_text)

    def get_chapter_number_from_file(self) -> int:
        """function to get chapter number out of file name"""
        first_number = self.__get_first_number(self.name)
        return int(first_number)

    def get_season_episode_from_file_name(self) -> str:
        """function to get season and episode from file name"""
        season_episode_matches = self.__get_season_episode_matches()
        return season_episode_matches

    def get_episode_from_file_name(self) -> str:
        season_episode_matches = self.__get_episode_matches()
        return season_episode_matches


@dataclass
class ServiceArguments:
    directory_in: str
    directory_out: str
    start_number: str = ""
    story: str = "n/a"
    chapter: str = "1"
    organization_file: str = "organize_chapters_to_vol.json"
    season_number: str = "1"
    extension: str = "mkv"


@dataclass
class ServiceMetaData:
    """class for holding meta data for ebook settings"""

    directory_in: str
    directory_out: str
    service: Callable
