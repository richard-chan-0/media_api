def prepend_zeros(number: int, number_zeros: int = 3) -> str:
    """function to add zeros until number matches format [0-9]+"""
    str_number = str(number)
    while len(str_number) < number_zeros:
        str_number = f"0{str_number}"

    return f"{str_number}"


def create_calibre_image_name(story: str, chapter: str, page: int) -> str:
    """function to generate name that can be read by calibre"""
    chapter_number = prepend_zeros(chapter)
    page_number = prepend_zeros(page)

    return f"{story} - c{chapter_number} - p{page_number}.png"


def create_seasoned_video_jellyfin_episode_name(season_name: str) -> str:
    """function to create an episode name in jellyfin format"""
    return f"Episode {season_name}.mkv"


def create_episode_video_jellyfin_episode_name(
    season_number: int, episode_number: int
) -> str:
    """function to create an episode name in jellyfin format with episode and season"""
    jellyfin_number_zeros = 2
    season = prepend_zeros(season_number, jellyfin_number_zeros)
    episode = prepend_zeros(episode_number, jellyfin_number_zeros)
    season_name = f"S{season}E{episode}"

    return create_seasoned_video_jellyfin_episode_name(season_name)
