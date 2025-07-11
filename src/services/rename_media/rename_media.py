from src.lib.service_constants import *
from src.lib.dataclasses import ServiceMetaData
from src.lib.utilities.app_functions import deprecate_function
from src.lib.utilities.os_functions import (
    rename_page_images,
    get_files,
    get_sorted_files,
    create_new_file_path,
)
from src.lib.utilities.name_functions import (
    create_calibre_image_name,
    create_jellyfin_episode_name,
    create_jellyfin_comic_name,
    cleanup_filename,
)
from src.lib.exceptions.exceptions import RenameMediaError
from src.lib.dataclasses import DirectoryFile, ServiceArguments
from typing import Iterable, Callable
import logging

logger = logging.getLogger(__name__)


def get_start_index(start_number: str) -> int:
    """function to get the start index for numbering files"""
    return (
        0 if (not start_number or not start_number.isnumeric()) else int(start_number)
    )


def get_buffer(start_index: str) -> int:
    """function to get the buffer for numbering files"""
    return 1 if start_index == 0 else 0


def create_rename_mapping_with_sorted(
    files: Iterable[DirectoryFile],
    directory: str,
    create_name_function: Callable,
    name_args: dict,
    start_number: str,
):
    """function to create a mapping between old file path and new file path for rename"""
    start_index = get_start_index(start_number)
    buffer = get_buffer(start_index)

    rename_mapping = {}
    logger.info(f"creating new names for files")
    for index, file in enumerate(files):
        file_number = index + start_index + buffer
        new_name = create_name_function(file_number, **name_args)
        new_path = create_new_file_path(directory, new_name)
        rename_mapping[file.path] = new_path

    return rename_mapping


def create_rename_mapping_with_filename(
    files: Iterable[DirectoryFile],
    directory_out: str,
    create_name_function: Callable,
    name_function_seed: str,
):
    """function to create a mapping between old file path and new file path for rename"""
    rename_mapping = {}
    for file in files:
        new_name = create_name_function(name_function_seed, file)
        new_path = create_new_file_path(directory_out, new_name)
        rename_mapping[file.path] = new_path

    return rename_mapping


def rename_image_to_calibre_image(args: ServiceArguments):
    deprecate_function()
    directory_in = args.directory_in
    directory_out = args.directory_out

    directory_entries = get_files(directory_in)
    rename_page_images(directory_out, directory_entries, create_calibre_image_name)


def create_jellyfin_episodes_mapping_with_seasoned_name(args):
    """renames a list of files in designated directory to jellyfin name with S[0-9][0-9]E[0-9][0-9] format"""
    deprecate_function()
    directory_in = args.directory_in
    directory_out = args.directory_out

    directory_entries = get_files(directory_in)
    rename_mapping = {}
    for entry in directory_entries:
        season_episode = entry.get_season_episode_from_file_name()
        if not season_episode:
            raise RenameMediaError(
                "file found in list that doesn't have name with a season episode (S00E00)"
            )

        new_name = create_jellyfin_episode_name(season_episode)
        new_path = create_new_file_path(directory_out, new_name)
        rename_mapping[entry.path] = new_path

    return rename_mapping


def create_jellyfin_episodes_mapping(args: ServiceArguments):
    """function to create the file names into jellyfin name"""
    directory = args.directory_in
    season_number = args.season_number
    start_number = args.start_number
    extension = args.extension

    filename_args = {
        "extension": extension,
        "season_number": int(season_number) if season_number else 1,
    }

    directory_entries = get_sorted_files(directory)
    return create_rename_mapping_with_sorted(
        files=directory_entries,
        directory=directory,
        create_name_function=create_jellyfin_episode_name,
        name_args=filename_args,
        start_number=start_number,
    )


def create_jellyfin_comics_mapping(args: ServiceArguments):
    """function to create mapping for cbz files into jellyfin comic name schema"""
    sort_method = lambda entry: entry.get_chapter_number_from_file()
    directory = args.directory_in
    story_name = args.story
    start_number = args.start_number

    filename_args = {"story_name": story_name}

    if not story_name:
        raise RenameMediaError("environment variable for story is empty")

    directory_entries = get_sorted_files(directory, sort_method)
    return create_rename_mapping_with_sorted(
        directory_entries,
        directory,
        create_jellyfin_comic_name,
        filename_args,
        start_number,
    )


def create_cleaned_filenames_mapping(args: ServiceArguments):
    """function to get mapping of old and new names for cleaning up the names for files"""
    directory_in = args.directory_in
    directory_out = args.directory_out
    story_name = args.story

    directory_entries = get_sorted_files(directory_in)

    return create_rename_mapping_with_filename(
        directory_entries,
        directory_out,
        cleanup_filename,
        story_name,
    )
