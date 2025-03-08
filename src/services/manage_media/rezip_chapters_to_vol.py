from zipfile import ZipFile
import src.lib.utilities.os_functions as SystemUtilities
from src.lib.exceptions.exceptions import RezipChaptersToVolError
import logging
from src.lib.dataclasses import DirectoryFile, ServiceArguments

from typing import Iterable

logger = logging.getLogger(__name__)
TEMP_FOLDER = "temp"


def create_volume_from_pages(
    pages: Iterable[DirectoryFile], directory_out: str, volume_name: str
):
    """function to create volume from page files"""
    logger.info("zipping pages into volume")
    volume_path = SystemUtilities.create_new_file_path(directory_out, volume_name)
    SystemUtilities.create_zip_file(volume_path, pages)

    return volume_path


def clean_system(temp_path: str, chapters: Iterable[DirectoryFile]):
    """function to clean files after creating volume file"""
    logger.info("removing temporary folder")
    SystemUtilities.remove_directory(temp_path)

    logger.info("removing chapter files from directory")
    for chapter in chapters:
        SystemUtilities.remove_file(chapter.path)

    logger.info("app folders are cleaned")


def move_pages_to_temp(directory_in: str, temp_path: str):
    """function to move pages into temp folder"""
    logger.info("migrating page files into temporary folder")
    images = SystemUtilities.get_images(directory_in)

    return SystemUtilities.move_files(images, temp_path)


def rezip_chapters_to_vol(args):
    """function that processes multiple cbz files into single cbz file"""
    directory_in = args.directory_in
    directory_out = args.directory_out
    volume_name = args.volume_name

    logger.info("creating temp folder")
    temp_path = SystemUtilities.create_sub_directory(directory_in, TEMP_FOLDER)

    logger.info("creating volume file: %s", volume_name)
    chapters = SystemUtilities.get_files(directory_in)

    logger.info("collecting pages from chapter files")
    try:
        SystemUtilities.extract_zip_file_content(directory_in, chapters)
    except Exception as e:
        raise RezipChaptersToVolError(e)

    pages = move_pages_to_temp(directory_in, temp_path)

    volume_path = create_volume_from_pages(pages, directory_out, volume_name)
    print(f"pages written to volume: {volume_path}")

    clean_system(temp_path, chapters)


def main(args: ServiceArguments):
    """service to open list of zip files and compile them into single zip file"""
    rezip_chapters_to_vol(args)
