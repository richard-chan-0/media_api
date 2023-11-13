from src.utilities.os_functions import (
    rename_page_images,
    get_files,
    rename_files,
)
from src.rename_media.name_functions import (
    create_calibre_image_name,
    create_seasoned_video_jellyfin_episode_name,
    create_episode_video_jellyfin_episode_name,
)
from src.exceptions.exceptions import RenameMediaError
from src.data_types.system_files import DirectoryFile
from typing import Iterable
from src.utilities.os_functions import get_env


class RenameService:
    def rename_image_to_calibre_image(directory_in, directory_out):
        # TODO: test if this still works
        directory_entries = get_files(directory_in)
        rename_page_images(directory_out, directory_entries, create_calibre_image_name)

    def rename_seasoned_video_to_jellyfin_name(directory_in: str, directory_out: str):
        """renames a list of files in designated directory to jellyfin name with S[0-9][0-9]E[0-9][0-9] format"""
        directory_entries = get_files(directory_in)
        rename_mapping = {}
        for entry in directory_entries:
            season_episode = entry.get_season_episode_from_file_name()
            if not season_episode:
                raise RenameMediaError(
                    "file found in list that doesn't have name with a season episode (S00E00)"
                )

            new_name = create_seasoned_video_jellyfin_episode_name(season_episode)
            new_path = f"{directory_out}/{new_name}"
            rename_mapping[entry.path] = new_path

        rename_files(rename_mapping)

    def rename_files_into_list_of_episodes(directory_in, directory_out):
        """function to indiscriminately rename the files in a season folder into jellyfin name"""
        directory_entries = get_files(directory_in)
        directory_entries.sort(key=lambda entry: entry.name)
        season_number = get_env("SEASON_NUMBER")
        rename_mapping = {}
        for list_index, episode in enumerate(directory_entries):
            episode_number = list_index + 1
            new_name = create_episode_video_jellyfin_episode_name(
                season_number, episode_number
            )
            new_path = f"{directory_out}/{new_name}"
            rename_mapping[episode.path] = new_path

        rename_files(rename_mapping)
