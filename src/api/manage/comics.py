from src.lib.utilities.app_functions import get_files_from_request
from src.lib.utilities.name_functions import create_jellyfin_comic_name
from src.lib.service_constants import (
    IMAGES_IN,
    IMAGES_OUT,
)
from src.lib.dataclasses.app import ServiceArguments
from src.services.manage_media.rezip_chapters_to_vol import rezip_chapters_to_vol


def rezip_chapters_to_volume(request):
    form = request.form
    volume_name = create_jellyfin_comic_name(
        issue=form["issue number"], story_name=form["story title"]
    )
    args = ServiceArguments(
        **{
            "directory_in": IMAGES_IN,
            "directory_out": IMAGES_OUT,
            "volume": volume_name,
        }
    )

    get_files_from_request(request, "files")
    rezip_chapters_to_vol(args)
    return f"files zipped into {volume_name}"
