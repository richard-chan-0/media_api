from src.lib.dataclasses import ComicRequest, ServiceArguments
from src.lib.utilities.os_functions import join_path
from src.lib.service_constants import IMAGES_IN, IMAGES_OUT
from src.services.rename_media.rename_media import create_jellyfin_comics_mapping


def get_jellyfin_comic_names_from_files(request):
    comic_request = ComicRequest(**request.form)
    files = request.files.getlist("files")

    for file in files:
        file_path = join_path(IMAGES_IN, file.filename)
        file.save(file_path)

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
