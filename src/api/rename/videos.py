from src.lib.dataclasses import VideoRequest, ServiceArguments
from src.lib.service_constants import INPUT_DIRECTORY, OUTPUT_DIRECTORY
from src.services.rename_media.rename_media import create_jellyfin_episodes_mapping
from src.lib.utilities.app_functions import get_files_from_request
from src.lib.factories.factories import create_video_request


def get_jellyfin_video_names_from_request(request):
    video_request = create_video_request(request)
    get_files_from_request(request, "files")

    return create_jellyfin_episodes_mapping(
        ServiceArguments(
            **{
                "directory_in": INPUT_DIRECTORY,
                "directory_out": OUTPUT_DIRECTORY,
                "start_number": video_request.start_number,
                "season_number": video_request.season_number,
            }
        )
    )
