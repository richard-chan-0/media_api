from dotenv import load_dotenv
from src.utilities.os_functions import (
    get_env,
    create_sub_directory,
    transfer_files,
)
from src.services import return_service
from src.guis import return_gui
from src.data_types.ServiceMetaData import ServiceMetaData
from src.data_types.ServiceArguments import ServiceArguments
from src.exceptions.exceptions import ServiceError

from src.tkinter.rename_gui import RenameGui
import logging
from src.ffmpeg.ffmpeg_functions import *

logger = logging.getLogger(__name__)

load_dotenv()


def pull_downloads(directory_in):
    """function to pull downloads from directory given env var"""
    download_dir = get_env("DOWNLOAD_DIR")
    if not download_dir:
        return
    transfer_files(download_dir, directory_in)


def configure_environment(utility_type: str) -> ServiceMetaData:
    """configures application environment"""
    logger.info("configuring environment")
    service_meta_data: ServiceMetaData = return_service(utility_type)

    directory_in = service_meta_data.directory_in
    directory_out = service_meta_data.directory_out

    logger.info("creating any missing directories")
    create_sub_directory(".", directory_in)
    create_sub_directory(".", directory_out)

    return service_meta_data


def main(utility_type):
    """main function for utility"""
    logger.info("retrieving service")

    service_metadata = configure_environment(utility_type)
    pull_downloads(service_metadata.directory_in)

    service_args = ServiceArguments(
        service_metadata.directory_in,
        service_metadata.directory_out,
        get_env("STORY"),
        get_env("CHAPTER"),
        get_env("ORGANIZATION_FILE"),
        get_env("SEASON_NUMBER"),
    )

    try:
        service_metadata.service(service_args)
    except ServiceError as err:
        logger.error(err)


def main_gui(utility_type):
    """main function for utility"""
    logger.info("retrieving service")
    configure_environment(utility_type)

    gui = return_gui(utility_type)
    service = gui()
    service.start()


def ffmpeg_main():
    streams = get_media_streams("images_out/Episode S01E01.mkv")
    stream_objs = parse_streams(streams)
    print(stream_objs)


if __name__ == "__main__":
    utility_type = get_env("UTILITY_TYPE")
    main_gui(utility_type)
    # ffmpeg_main()
