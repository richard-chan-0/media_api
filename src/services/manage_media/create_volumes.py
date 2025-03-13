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


def create_volume(volume_path: str, chapter_files_path: str, volume_name: str):
    """function to create volume file using files in a volume directory"""
    chapters = get_files(chapter_files_path)
    move_files(chapters, volume_path)

    rezip_chapters_to_vol(volume_path, volume_name)

    remove_directory(chapter_files_path)


def create_volumes(args: ServiceArguments):
    """creates set of volume files from list of chapters"""
    volume_folders = create_volume_directories(
        args.story, args.directory_in, args.volume_mapping
    )
    for folder in volume_folders:
        create_volume(args.directory_out, folder.path, volume_name=f"{folder.name}")
