# using 'import' to resolve circular import issue
import src.services as AppServices

from src.rezip_chapters_to_vol.rezip_chapters_to_vol import rezip_chapters_to_vol
from src.utilities.os_functions import (
    get_sub_directories,
    get_files,
    move_files,
    remove_directory,
)
import logging

logger = logging.getLogger(__name__)


def get_chapters_for_volumes(services):
    """creates volume folders and moves corresponding chapter files"""
    organize_service_data = services[AppServices.ORGANIZE_CHAPTERS_TO_VOL_NAME]
    service = organize_service_data.service
    directory_in = organize_service_data.directory_in
    directory_out = organize_service_data.directory_out

    service(directory_in, directory_out)

    return get_sub_directories(directory_out)


def create_volume(services: dict, chaper_files_path: str, volume_name: str):
    """function to create volume file using files in a volume directory"""
    rezip_service_data = services[AppServices.REZIP_CHAPTERS_TO_VOL_NAME]

    directory_in = rezip_service_data.directory_in
    directory_out = rezip_service_data.directory_out

    chapters = get_files(chaper_files_path)
    move_files(chapters, rezip_service_data.directory_in)

    rezip_chapters_to_vol(directory_in, directory_out, volume_name)

    remove_directory(chaper_files_path)


def create_volumes():
    """creates set of volume files from list of chapters"""
    services = AppServices.get_services()
    volume_folders = get_chapters_for_volumes(services)

    for folder in volume_folders:
        zip_name = f"{folder.name}.cbz"
        create_volume(services, folder.path, zip_name)


def main(directory_in, directory_out):
    """service to take list of cbz files and produce volume files"""
    create_volumes()
