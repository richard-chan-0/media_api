from src.services.manage_media.organize_chapters_to_vol import (
    organize_chapters_to_vol,
)
from src.services.manage_media.rezip_chapters_to_vol import rezip_chapters_to_vol
from src.lib.dataclasses import ServiceArguments
from src.lib.utilities.os_functions import (
    get_sub_directories,
    get_files,
    move_files,
    remove_directory,
)
import logging

logger = logging.getLogger(__name__)


def create_volume_directories(story_title, directory_in, volume_mapping):
    """creates volume folders and moves corresponding chapter files"""
    organize_chapters_to_vol(story_title, directory_in, volume_mapping)

    return get_sub_directories(directory_in)


def create_volume(
    volume_path: str, chapter_files_path: str, volume_name: str, ignore_files=[]
):
    """function to create volume file using files in a volume directory"""
    logger.info(f"Creating volume: {volume_name} at {volume_path}")
    chapters = get_files(chapter_files_path)
    logger.info(f"Found {len(chapters)} chapters in {chapter_files_path}")
    move_files(chapters, volume_path)
    logger.info(f"Moved chapters to {volume_path}")

    rezip_chapters_to_vol(volume_path, volume_name, ignore_files)
    remove_directory(chapter_files_path)


def create_volumes(args: ServiceArguments):
    """creates set of volume files from list of chapters"""
    volume_folders = create_volume_directories(
        args.story, args.directory_in, args.volume_mapping
    )
    ignore_files = []
    # TODO: fix this
    for folder in volume_folders:
        create_volume(
            args.directory_in,
            folder.path,
            volume_name=f"{folder.name.replace('-folder', '')}",
            ignore_files=ignore_files,
        )
