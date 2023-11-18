from src.utilities.os_functions import (
    rename_page_images,
    get_files,
    rename_files,
    get_sorted_files,
    create_new_file_path,
)
from src.rename_media.name_functions import (
    create_calibre_image_name,
    create_jellyfin_episode_name,
    create_jellyfin_comic_name,
    cleanup_filename,
)
from src.exceptions.exceptions import RenameMediaError
from src.data_types.DirectoryFile import DirectoryFile
from src.data_types.ServiceArguments import ServiceArguments
from typing import Iterable, Callable


def create_rename_mapping_with_sorted(
    files: Iterable[DirectoryFile],
    directory_out: str,
    create_name_function: Callable,
    name_function_seed: str,
):
    """function to create a mapping between old file path and new file path for rename"""
    rename_mapping = {}
    for list_index, file in enumerate(files):
        episode_number = list_index + 1
        new_name = create_name_function(name_function_seed, episode_number)
        new_path = create_new_file_path(directory_out, new_name)
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
    directory_in = args.directory_in
    directory_out = args.directory_out

    directory_entries = get_files(directory_in)
    rename_page_images(directory_out, directory_entries, create_calibre_image_name)


def rename_seasoned_video_to_jellyfin_name(args: ServiceArguments):
    """renames a list of files in designated directory to jellyfin name with S[0-9][0-9]E[0-9][0-9] format"""
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

    rename_files(rename_mapping)


def rename_files_into_list_of_jellyfin_episodes(args: ServiceArguments):
    """function to indiscriminately rename the files in a season folder into jellyfin name"""
    directory_in = args.directory_in
    directory_out = args.directory_out
    season_number = args.season_number

    if not season_number:
        raise RenameMediaError("environment variable for season is empty")

    directory_entries = get_sorted_files(directory_in)
    rename_mapping = create_rename_mapping_with_sorted(
        directory_entries,
        directory_out,
        create_jellyfin_episode_name,
        int(season_number),
    )

    rename_files(rename_mapping)


def rename_files_into_list_of_jellyfin_comics(args: ServiceArguments):
    """function to indiscriminately rename the files in a season folder into jellyfin name"""
    sort_method = lambda entry: entry.get_chapter_number_from_file()
    directory_in = args.directory_in
    directory_out = args.directory_out
    story_name = args.story

    if not story_name:
        raise RenameMediaError("environment variable for story is empty")

    directory_entries = get_sorted_files(directory_in, sort_method)
    rename_mapping = create_rename_mapping_with_sorted(
        directory_entries,
        directory_out,
        create_jellyfin_comic_name,
        story_name,
    )

    rename_files(rename_mapping)


def rename_files_to_clean_up_downloads(args: ServiceArguments):
    """function to clean up file names of tags or metadata in name"""
    directory_in = args.directory_in
    directory_out = args.directory_out
    story_name = args.story

    directory_entries = get_sorted_files(directory_in)

    rename_mapping = create_rename_mapping_with_filename(
        directory_entries,
        directory_out,
        cleanup_filename,
        story_name,
    )

    rename_files(rename_mapping)
