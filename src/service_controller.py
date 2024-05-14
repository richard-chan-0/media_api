import src.services.rename_media.rename_media as RenameService
from src.services.manage_media.organize_chapters_to_vol import (
    main as organize_chapters_to_vol,
)
from src.services.manage_media.rezip_chapters_to_vol import (
    main as rezip_chapters_to_vol,
)

from src.services.manage_media.create_volumes import create_volumes
from src.lib.data_types.ServiceMetaData import ServiceMetaData
from src.lib.exceptions.exceptions import InvalidService
from typing import Iterable
from src.lib.data_types.service_constants import *


def get_list_service() -> Iterable[str]:
    """function to get list of service names"""
    return [key for key in get_services().keys()]


def get_services() -> dict[str, ServiceMetaData]:
    """returns mapping of service names to service metadata"""
    return {
        **RenameService.rename_services,
        ORGANIZE_CHAPTERS_TO_VOL_NAME: ServiceMetaData(
            "chapter_pdf_in", "chapter_pdf_out", organize_chapters_to_vol
        ),
        REZIP_CHAPTERS_TO_VOL_NAME: ServiceMetaData(
            IMAGES_IN, IMAGES_OUT, rezip_chapters_to_vol
        ),
        CREATE_VOLUMES_NAME: ServiceMetaData(None, None, create_volumes),
        "ffmpeg": ServiceMetaData(None, None, None),
    }


def return_service(service_name: str) -> ServiceMetaData:
    """returns service"""
    services = get_services()

    if service_name not in services:
        raise InvalidService(f"{service_name} is not valid service")

    return services[service_name]
