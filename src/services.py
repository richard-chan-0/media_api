import src.rename_media.rename_media as RenameService
from src.organize_media.organize_chapters_to_vol import (
    main as organize_chapters_to_vol,
)
from src.rezip_cbz_files.rezip_chapters_to_vol import (
    main as rezip_chapters_to_vol,
)
from src.prepare_for_jellyfin.prepare_for_jellyfin import main as prepare_for_jellyfin
from src.create_volumes.create_volumes import main as create_volumes
from src.data_types.ServiceMetaData import ServiceMetaData
from src.exceptions.exceptions import InvalidService

ORGANIZE_CHAPTERS_TO_VOL_NAME = "organize_chapters_to_vol"
RENAME_TO_CALIBRE_IMAGE = "create_calibre_image_name"
RENAME_SEASONED_TO_JELLY_NAME = "rename_seasoned_video_to_jellyfin_name"
RENAME_FILES_TO_JELLY_EPISODES = "rename_files_into_list_of_jellyfin_episodes"
RENAME_FILES_TO_JELLY_COMICS = "rename_files_to_list_of_jellyfin_comic"
SCRAPE_FOR_VOL_TO_CHAPTERS_NAME = "scrape_for_vol_to_chapters"
REZIP_CHAPTERS_TO_VOL_NAME = "rezip_chapters_to_vol"
CREATE_VOLUMES_NAME = "create_volumes"
PREPARE_FOR_JELLYFIN = "prepare_for_jellyfin"
IMAGES_IN = "images_in"
IMAGES_OUT = "images_out"


def get_services() -> dict[str, ServiceMetaData]:
    """returns mapping of service names to service metadata"""
    return {
        RENAME_TO_CALIBRE_IMAGE: ServiceMetaData(
            IMAGES_IN, IMAGES_OUT, RenameService.rename_image_to_calibre_image
        ),
        RENAME_SEASONED_TO_JELLY_NAME: ServiceMetaData(
            IMAGES_IN,
            IMAGES_OUT,
            RenameService.rename_seasoned_video_to_jellyfin_name,
        ),
        RENAME_FILES_TO_JELLY_EPISODES: ServiceMetaData(
            IMAGES_IN,
            IMAGES_OUT,
            RenameService.rename_files_into_list_of_jellyfin_episodes,
        ),
        RENAME_FILES_TO_JELLY_COMICS: ServiceMetaData(
            IMAGES_IN,
            IMAGES_OUT,
            RenameService.rename_files_into_list_of_jellyfin_comics,
        ),
        ORGANIZE_CHAPTERS_TO_VOL_NAME: ServiceMetaData(
            "chapter_pdf_in", "chapter_pdf_out", organize_chapters_to_vol
        ),
        REZIP_CHAPTERS_TO_VOL_NAME: ServiceMetaData(
            "chapter_zip_in", "chapter_zip_out", rezip_chapters_to_vol
        ),
        CREATE_VOLUMES_NAME: ServiceMetaData(None, None, create_volumes),
        PREPARE_FOR_JELLYFIN: ServiceMetaData(
            IMAGES_IN, IMAGES_OUT, prepare_for_jellyfin
        ),
    }


def return_service(service_name: str) -> ServiceMetaData:
    """returns service"""
    services = get_services()

    if service_name not in services:
        raise InvalidService(f"{service_name} is not valid service")

    return services[service_name]
