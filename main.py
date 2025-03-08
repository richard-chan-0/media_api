from tkinter import *
from src.lib.utilities.os_functions import (
    create_sub_directory,
)

from src.gui_controller import return_gui
from src.lib.dataclasses import ServiceMetaData
from src.lib.utilities.app_functions import get_parser
import logging

logger = logging.getLogger(__name__)


def configure_environment() -> ServiceMetaData:
    """configures application environment"""
    logger.info("configuring environment")
    logger.info("creating any missing directories")
    create_sub_directory(".", "input")
    create_sub_directory(".", "output")


def main_gui(utility_type):
    """main function for utility"""
    logger.info("retrieving service")
    if not utility_type:
        return

    configure_environment()

    gui = return_gui(utility_type)
    root = Tk()
    service = gui(root)
    service.start()


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    utility_type = args.type

    main_gui(utility_type)
