from src.lib.exceptions.exceptions import OrganizeChaptersToVolError
from src.lib.utilities.os_functions import *
from src.lib.dataclasses import DirectoryFile
from json import load
from typing import Iterable, Tuple
from src.services.rename_media.rename_media import create_jellyfin_comic_name


VOLUMES = "volumes"
VOLUME = "volume"
START_CHAPTER = "startChapter"
END_CHAPTER = "endChapter"


def is_valid_chapter(chapter):
    """function to determine if chapter contains all attributes"""
    is_with_volume = VOLUME in chapter
    is_with_start = START_CHAPTER in chapter
    is_with_end = END_CHAPTER in chapter
    return all([is_with_end, is_with_start, is_with_volume])


def update_chapter_list(
    volume_path: str,
    moved_files: Iterable[DirectoryFile],
    chapters: Iterable[DirectoryFile],
):
    """function to remove chapters that have been moved"""
    volume_files = {"volume_path": volume_path, "chapters": []}
    for file in moved_files:
        volume_files["chapters"].append(file.name)
        chapters.remove(file)

    return volume_files


def move_chapters_for_volume_dir(
    volume_path: str,
    chapter_details: Tuple[str, str],
    chapters: Iterable[DirectoryFile],
):
    """function to move chapter files into a designated volume directory"""
    start_chapter, end_chapter = chapter_details
    moved_files = []

    for chapter in chapters:
        chapter_name = chapter.name
        chapter_path = chapter.path
        chapter_number = chapter.get_chapter_number_from_file()
        if not (int(start_chapter) <= chapter_number <= int(end_chapter)):
            continue

        new_path = create_new_file_path(volume_path, chapter_name)
        move_file(old_path=chapter_path, new_path=new_path)
        moved_files.append(chapter)

    return update_chapter_list(volume_path, moved_files, chapters)


def move_chapters_to_volumes(
    story_title: str,
    directory_out: str,
    chapters: Iterable[DirectoryFile],
    mapping: dict[str, Tuple[str, str]],
):
    """creates directories for volumes and moves files into those directories"""
    volumes = mapping["volumes"]
    for volume in volumes:
        volume_number = volume["volume"]
        volume_name = create_jellyfin_comic_name(
            issue=volume_number, story_name=story_title
        )
        chapter_details = (volume["startChapter"], volume["endChapter"])
        sub_directory = create_sub_directory(directory_out, volume_name)
        move_chapters_for_volume_dir(sub_directory, chapter_details, chapters)


def organize_chapters_to_vol(story_title, directory_in, volume_mapping):
    """function to move chapters into corresponding subdirectory folders as volumes"""
    chapters = get_files(path=directory_in)
    move_chapters_to_volumes(story_title, directory_in, chapters, volume_mapping)
