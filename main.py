from dotenv import load_dotenv
from src.utilities.os_functions import (
    get_env,
    create_sub_directory,
    transfer_files,
)
from src.services import return_service
from src.data_types.ServiceMetaData import ServiceMetaData
from src.data_types.ServiceArguments import ServiceArguments
from src.exceptions.exceptions import ServiceError

from src.tkinter.rename_gui import RenameGui
import logging

logger = logging.getLogger(__name__)

load_dotenv()


def configure_environment(directory_in: str, directory_out: str) -> None:
    """configures application environment"""
    download_dir = get_env("DOWNLOAD_DIR")
    transfer_files(download_dir, directory_in)

    logger.info("creating missing directories")
    create_sub_directory(".", directory_in)
    create_sub_directory(".", directory_out)


def main(utility_type):
    """main function for utility"""
    logger.info("retrieving service")
    service_meta_data: ServiceMetaData = return_service(utility_type)

    service = service_meta_data.service
    directory_in = service_meta_data.directory_in
    directory_out = service_meta_data.directory_out

    configure_environment(directory_in, directory_out)

    service_args = ServiceArguments(
        directory_in,
        directory_out,
        get_env("STORY"),
        get_env("CHAPTER"),
        get_env("ORGANIZATION_FILE"),
        get_env("SEASON_NUMBER"),
    )

    try:
        service(service_args)
    except ServiceError as err:
        logger.error(err)


if __name__ == "__main__":
    utility_type = get_env("UTILITY_TYPE")
    main(utility_type)
    # gui = RenameGui()
    # gui.start()
