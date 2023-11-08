from pytest import fixture
from src.organize_chapters_to_vol.organize_chapters_to_vol import (
    organize_chapters_to_vol,
)


@fixture
def json_file():
    return {
        "volumes": [
            {"volume": 1, "chapterStart": 1, "chapterEnd": 3},
            {"volume": 2, "chapterStart": 4, "chapterEnd": 6},
        ],
    }


def test_given_a_list_of_names_and_json_organize_file_names(json_file):
    pass


def test_round_partial_chapters_to_nearest_chapter(json_file):
    pass
