from src.lib.utilities.app_functions import get_files_from_request
from src.lib.utilities.name_functions import create_jellyfin_comic_name
from src.lib.service_constants import (
    PROCESS_DIRECTORY,
)
from src.lib.dataclasses.app import ServiceArguments
from src.services.manage_media.create_volumes import create_volumes
from json import loads


def run_create_volumes(request):
    form = request.form
    story_title = form["story title"]
    volume_mapping = loads(form["volume mapping"])
    args = ServiceArguments(
        **{
            "directory_in": PROCESS_DIRECTORY,
            "volume_mapping": volume_mapping,
            "story": story_title,
        }
    )

    get_files_from_request(request, "files")
    create_volumes(args)
    return f"new volumes created for story: {story_title}"
