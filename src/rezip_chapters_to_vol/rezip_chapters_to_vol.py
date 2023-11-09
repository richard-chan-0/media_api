from zipfile import ZipFile
import src.utilities.os_functions as SystemUtilities
from src.exceptions.exceptions import RezipChaptersToVolError
from posix import DirEntry
from typing import Iterable

TEMP_FOLDER = "temp"


def extract_pages_from_chapter(directory_in: str, chapters: Iterable[DirEntry]):
    """function to extract all page files from chapter files"""
    for chapter in chapters:
        if not SystemUtilities.is_compressed(chapter.name):
            continue

        with ZipFile(chapter, "r") as zip:
            zip.extractall(directory_in)


def move_pages_to_temp(directory_in: str, temp_path: str):
    """function to move pages into temp folder"""
    images = SystemUtilities.get_images(directory_in)
    page_paths = []

    for image in images:
        source = image.path
        destination = f"{temp_path}/{image.name}"
        SystemUtilities.move_file(source, destination)
        page_paths.append(destination)

    return page_paths


def create_volume_from_pages(
    pages: Iterable[DirEntry], directory_out: str, volume_name: str
):
    """function to create volume from page files"""
    volume_path = f"{directory_out}/{volume_name}"
    with ZipFile(volume_path, "w") as volume:
        for page in pages:
            try:
                volume.write(page)
            except Exception as err:
                raise RezipChaptersToVolError(err)

    return volume_path


def clean_system(temp_path, chapters):
    """function to clean files after creating volume file"""
    # remove temp folder
    SystemUtilities.remove_directory(temp_path)

    # remove zip files
    for chapter in chapters:
        SystemUtilities.remove_file(chapter.path)


def rezip_chapters_to_vol(directory_in, directory_out, volume_name: str = "temp.cbz"):
    """function that processes multiple cbz files into single cbz file"""
    # get all files
    chapters = SystemUtilities.get_files(directory_in)
    temp_path = SystemUtilities.make_sub_directory(directory_in, TEMP_FOLDER)

    extract_pages_from_chapter(directory_in, chapters)
    pages = move_pages_to_temp(directory_in, temp_path)

    volume_path = create_volume_from_pages(pages, directory_out, volume_name)
    print(f"pages written to volume: {volume_path}")

    clean_system(temp_path, chapters)


def main(directory_in, directory_out):
    """service to open list of zip files and compile them into single zip file"""
    rezip_chapters_to_vol(directory_in, directory_out)
