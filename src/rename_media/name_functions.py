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


def create_jellyfin_episode_name(season_number: int, episode_number: int) -> str:
    """function to create an episode name in jellyfin format with episode and season"""
    jellyfin_number_zeros = 2
    season = prepend_zeros(season_number, jellyfin_number_zeros)
    episode = prepend_zeros(episode_number, jellyfin_number_zeros)
    return f"Episode S{season}E{episode}.mkv"


def create_jellyfin_comic_name(story_name: str, issue: int) -> str:
    jellyfin_number_zeros = 2
    issue_number = prepend_zeros(issue, jellyfin_number_zeros)

    return f"{story_name} #{issue_number}.cbz"
