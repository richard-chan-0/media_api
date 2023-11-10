from src.exceptions.exceptions import OrganizeChaptersToVolError
from src.utilities.os_functions import *
from json import load
from typing import Iterable
from re import findall

VOLUMES = "volumes"
VOLUME = "volume"
START_CHAPTER = "startChapter"
END_CHAPTER = "endChapter"


def get_chapters_to_vols_data():
    file_name = get_organization_file()
    file = open(file_name)
    return load(file)


def is_valid_chapter(chapter):
    """function to determine if chapter contains all attributes"""
    is_with_volume = VOLUME in chapter
    is_with_start = START_CHAPTER in chapter
    is_with_end = END_CHAPTER in chapter
    return all([is_with_end, is_with_start, is_with_volume])


def create_mapping_chapters_to_vols():
    """returns content of json organization file"""
    schema = get_chapters_to_vols_data()
    if "volumes" not in schema:
        raise OrganizeChaptersToVolError("expected volumes attribute in schema")

    chapters = schema[VOLUMES]
    mapping = {}
    for chapter in chapters:
        if not is_valid_chapter(chapter):
            raise OrganizeChaptersToVolError("volume missing attribute")

        volume = chapter[VOLUME]
        start_chapter = chapter[START_CHAPTER]
        end_chapter = chapter[END_CHAPTER]
        mapping[volume] = (start_chapter, end_chapter)

    return mapping


def get_chapter_number_from_file(file_name):
    """function to get chapter number out of file name"""
    return findall("[0-9]+", file_name)


def write_chapters_for_volume(sub_directory, chapter_details, chapters: Iterable[str]):
    start_chapter, end_chapter = chapter_details
    moved_files = []
    for chapter in chapters:
        chapter_name = chapter.name
        chapter_path = chapter.path
        chapter_number = int(get_chapter_number_from_file(chapter_name)[0])
        if not (start_chapter <= chapter_number <= end_chapter):
            continue

        new_path = f"{sub_directory}/{chapter_name}"
        move_file(old_path=chapter_path, new_path=new_path)
        moved_files.append(chapter)

    for file in moved_files:
        chapters.remove(file)


def write_to_system(
    directory_out: str, chapters: Iterable[str], mapping: dict[str, str]
):
    """creates directories for volumes and moves files into those directories"""
    for volume, chapter_details in mapping.items():
        sub_directory = create_sub_directory(directory_out, volume)
        write_chapters_for_volume(sub_directory, chapter_details, chapters)


def organize_chapters_to_vol(directory_in: str, directory_out: str):
    """function to move chapters into corresponding subdirectory folders as volumes"""
    chapters = get_files(directory=directory_in)
    mapping = create_mapping_chapters_to_vols()
    write_to_system(directory_out, chapters, mapping)


def main(directory_in: str, directory_out: str):
    """main function for organizing files feature"""
    organize_chapters_to_vol(directory_in, directory_out)
