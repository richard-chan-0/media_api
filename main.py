from dotenv import load_dotenv
from tkinter import *
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
import logging

logger = logging.getLogger(__name__)

load_dotenv()


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


def main_gui(utility_type):
    """main function for utility"""
    logger.info("retrieving service")
    configure_environment(utility_type)

    gui = return_gui(utility_type)
    root = Tk()
    service = gui(root)
    service.start()


if __name__ == "__main__":
    utility_type = get_env("UTILITY_TYPE")
    main_gui(utility_type)
