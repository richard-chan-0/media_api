def prepend_zeros(number: int) -> str:
    """function to add zeros until number matches format [0-9][0-9][0-9]"""
    str_number = str(number)
    while len(str_number) < 3:
        str_number = f"0{str_number}"

    return f"{str_number}"


def create_calibre_image_name(story: str, chapter: str, page: int) -> str:
    """function to generate name that can be read by calibre"""
    chapter_number = prepend_zeros(chapter)
    page_number = prepend_zeros(page)

    return f"{story} - c{chapter_number} - p{page_number}.png"


def create_jellyfin_episode_name(season_name: str) -> str:
    """function to create an episode name in jellyfin format"""
    return f"Episode {season_name}.mkv"
