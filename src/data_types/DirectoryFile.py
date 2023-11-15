from dataclasses import dataclass
from re import findall, sub
from typing import Iterable


@dataclass
class DirectoryFile:
    """data structure"""

    name: str
    path: str

    def get_chapter_number_from_file(self) -> int:
        """function to get chapter number out of file name"""
        return int(findall("[0-9]+", self.name)[0])

    def __get_season_episode_matches(self) -> Iterable[str]:
        return findall("S[0-9][0-9]E[0-9]+", self.name)

    def __get_episode_matches(self) -> Iterable[str]:
        clean_resolution_text = sub("(720|1080|360|1920|1440)", "?", self.name)
        return findall("[0-9]+", clean_resolution_text)

    def __is_match_found(self, list_to_test: Iterable[str]) -> bool:
        """function to determine if file name contains a match from findall"""
        return bool(list_to_test)

    def get_season_episode_from_file_name(self) -> str:
        """function to get season and episode from file name"""
        season_episode_matches = self.__get_season_episode_matches()
        if not self.__is_match_found(season_episode_matches):
            return
        return season_episode_matches[0]

    def get_episode_from_file_name(self) -> str:
        season_episode_matches = self.__get_episode_matches()
        if not self.__is_match_found(season_episode_matches):
            return
        return season_episode_matches[0]
