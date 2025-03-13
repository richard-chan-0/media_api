from src.lib.utilities.app_functions import get_files_from_request
from src.lib.utilities.name_functions import create_jellyfin_comic_name
from src.lib.service_constants import (
    IMAGES_IN,
    IMAGES_OUT,
)
from src.lib.dataclasses.app import ServiceArguments
from src.services.manage_media.create_volumes import create_volumes
from json import loads


# TODO: fix this to use create volumes function instead
# TODO: create error handling with flask
def run_create_volumes(request):
    form = request.form
    volume_name = create_jellyfin_comic_name(
        issue=form["issue number"], story_name=form["story title"]
    )
    volume_mapping = loads(form["volume mapping"])
    args = ServiceArguments(
        **{
            "directory_in": IMAGES_IN,
            "directory_out": IMAGES_OUT,
            "volume": volume_name,
            "volume_mapping": volume_mapping,
        }
    )

    get_files_from_request(request, "files")
    create_volumes(args)
    return f"files zipped into {volume_name}"
