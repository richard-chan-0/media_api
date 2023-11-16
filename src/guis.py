from src.tkinter.gui import Gui
from src.data_types.service_constants import *
from src.tkinter.rename_gui import RenameGui
from src.exceptions.exceptions import InvalidService


def get_services_gui() -> Gui:
    """returns mapping of service names to service metadata"""
    return {
        RENAME_TO_CALIBRE_IMAGE: RenameGui,
        RENAME_SEASONED_TO_JELLY_NAME: RenameGui,
        RENAME_FILES_TO_JELLY_EPISODES: RenameGui,
        RENAME_FILES_TO_JELLY_COMICS: RenameGui,
    }


def return_gui(service_name: str) -> Gui:
    """returns service"""
    services = get_services_gui()

    if service_name not in services:
        raise InvalidService(f"{service_name} is not valid service")

    return services[service_name]
