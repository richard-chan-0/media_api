from src.lib.dataclasses import ComicRequest, ServiceArguments
from src.lib.service_constants import IMAGES_IN, IMAGES_OUT
from src.services.rename_media.rename_media import create_jellyfin_comics_mapping
from src.lib.utilities.app_functions import get_files_from_request


def get_jellyfin_comic_names_from_files(request):
    comic_request = ComicRequest(**request.form)
    get_files_from_request(request, "files")

    return create_jellyfin_comics_mapping(
        ServiceArguments(
            **{
                "directory_in": IMAGES_IN,
                "directory_out": IMAGES_OUT,
                "story": comic_request.comic_name,
                "start_number": comic_request.start_number,
            }
        )
    )
