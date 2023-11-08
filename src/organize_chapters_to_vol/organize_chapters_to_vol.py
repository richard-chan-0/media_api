from src.exceptions.exceptions import ServiceError, OrganizeChaptersToVolError
from src.utilities.os_functions import *
from json import load
from typing import Iterable
from re import findall


def get_mapping_data():
    file_name = get_organization_file()
    file = open(file_name)
    return load(file)


def create_mapping_chapters_to_vols():
    """returns content of json organization file"""
    schema = get_mapping_data()
    chapters = schema["chapters"]
    mapping = {}
    for chapter in chapters:
        chapter_number = chapter["chapter"]
        volume_number = chapter["volume"]
        mapping[chapter_number] = volume_number

    return mapping


def get_chapter_number_from_file(file_name):
    """function to get chapter number out of file name"""
    return findall("[0-9]+", file_name)


def write_to_system(
    directory_out: str, chapters: Iterable[str], mapping: dict[str, str]
):
    """creates directories for volumes and moves files into those directories"""
    for chapter in chapters:
        chapter_name = chapter.name
        chapter_path = chapter.path

        chapter_number = get_chapter_number_from_file(chapter_name)[0]
        if chapter_number not in mapping:
            continue
        print(f"moving chapter {chapter_number} into folder {mapping[chapter_number]}")
        volume = mapping[chapter_number]
        sub_directory = make_sub_directory(directory_out, volume)
        new_path = f"{sub_directory}/{chapter_name}"
        move_file(old_path=chapter_path, new_path=new_path)


def organize_chapters_to_vol(directory_in: str, directory_out: str):
    """function to move chapters into corresponding subdirectory folders as volumes"""
    chapters = get_files(directory=directory_in)
    mapping = create_mapping_chapters_to_vols()
    write_to_system(directory_out, chapters, mapping)


def main(directory_in: str, directory_out: str):
    """main function for organizing files feature"""
    try:
        organize_chapters_to_vol(directory_in, directory_out)
    except Exception as err:
        if isinstance(err, OrganizeChaptersToVolError):
            print("error occurred when organizing files")
        raise ServiceError(err)
