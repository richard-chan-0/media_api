import src.rename_media.name_functions as NameFunctions
from src.exceptions.exceptions import RenameMediaError
from pytest import raises


def test_numbers_less_than_three_digits_has_zeros():
    test_number = 3
    result = NameFunctions.prepend_zeros(test_number)
    assert result == "003"


def test_numbers_more_than_three_digits_returns_same_number():
    test_number = 3141

    result = NameFunctions.prepend_zeros(test_number)

    assert result == "3141"


def test_name_produces_correct_file_name():
    story = "Spy x Family"
    chapter = "2"
    page = 1

    result = NameFunctions.create_calibre_image_name(story, chapter, page)

    assert result == "Spy x Family - c002 - p001.png"


def test_create_jellyfin_episode_name_happy_path():
    season_number = 1
    episode_number = 1
    expected = "Episode S01E01.mkv"

    result = NameFunctions.create_jellyfin_episode_name(season_number, episode_number)

    assert result == expected


def test_create_jellyfin_episode_name_raise_error_for_negative():
    season_number = -1
    episode_number = 1

    with raises(RenameMediaError):
        NameFunctions.create_jellyfin_episode_name(season_number, episode_number)
