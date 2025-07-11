from src.lib.dataclasses import ServiceArguments
from src.lib.service_constants import PROCESS_DIRECTORY
from src.services.rename_media.rename_media import create_jellyfin_comics_mapping
from src.lib.utilities.app_functions import get_files_from_request
from src.lib.factories.factories import create_comic_request


def get_jellyfin_comic_names_from_files(request):
    comic_request = create_comic_request(request)
    get_files_from_request(request, "files")

    return create_jellyfin_comics_mapping(
        ServiceArguments(
            **{
                "directory_in": PROCESS_DIRECTORY,
                "story": comic_request.comic_name,
                "start_number": comic_request.start_number,
            }
        )
    )
