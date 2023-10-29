from .rename_chapters.rename_chapters import main as rename_chapters
from .organize_chapters_to_vol.organize_chapters_to_vol import (
    main as organize_chapters_to_vol,
)
from .data_types.ServiceMetaData import ServiceMetaData
from .exceptions.exceptions import InvalidService


def get_services() -> dict:
    """returns mapping of service names to service metadata"""
    return {
        "rename_chapters": ServiceMetaData("images_in", "images_out", rename_chapters),
        "organize_chapters_to_vol": ServiceMetaData(
            "chapter_pdf_in", "chapter_pdf_out", organize_chapters_to_vol
        ),
    }


def return_service(service_name: str) -> ServiceMetaData:
    """returns service"""
    services = get_services()

    if service_name not in services:
        raise InvalidService(f"{service_name} is not valid service")

    return services[service_name]
