from os import getenv

ORGANIZE_CHAPTERS_TO_VOL_NAME = "organize_chapters_to_vol"
RENAME_TO_CALIBRE_IMAGE = "create_calibre_image_name"
RENAME_SEASONED_TO_JELLY_NAME = "rename_seasoned_video_to_jellyfin_name"
RENAME_FILES_TO_JELLY_EPISODES = "rename_files_into_list_of_jellyfin_episodes"
RENAME_FILES_TO_JELLY_COMICS = "rename_files_to_list_of_jellyfin_comic"
SCRAPE_FOR_VOL_TO_CHAPTERS_NAME = "scrape_for_vol_to_chapters"
REZIP_CHAPTERS_TO_VOL_NAME = "rezip_chapters_to_vol"
CREATE_VOLUMES_NAME = "create_volumes"
PREPARE_FOR_JELLYFIN = "prepare_for_jellyfin"
RENAME_TO_CLEANUP = "rename_files_to_clean_up_downloads"
PROCESS_DIRECTORY = getenv("PROCESS_DIRECTORY")

INTERNAL_SERVER_ERROR_CODE = 500
BAD_REQUEST_CODE = 400
