from src.utilities.os_functions import (
    rename_page_images,
    get_files,
    rename_mkv_video_files,
)
from src.rename_chapters.name_functions import (
    create_calibre_image_name,
    create_jellyfin_episode_name,
)


def rename(directory_in, directory_out):
    # TODO: test if this still works
    directory_entries = get_files(directory_in)
    rename_page_images(directory_out, directory_entries, create_calibre_image_name)


def rename_videos_with_seasons(directory_in, directory_out):
    directory_entries = get_files(directory_in)
    rename_mkv_video_files(
        directory_out, directory_entries, create_jellyfin_episode_name
    )


def main(directory_in, directory_out):
    """main logic for utility"""
    rename_videos_with_seasons(directory_in, directory_out)
