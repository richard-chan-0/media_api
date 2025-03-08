from pytest import fixture
from src.services.manage_media.organize_chapters_to_vol import update_chapter_list
from src.lib.factories.factories import create_file


@fixture
def json_file():
    return {
        "volumes": [
            {"volume": 1, "chapterStart": 1, "chapterEnd": 3},
            {"volume": 2, "chapterStart": 4, "chapterEnd": 6},
        ],
    }


def test_remove_files_from_list():
    volume_path = "volume path"
    chapters = [create_file(i, "") for i in range(5)]
    moved_files = chapters[:3]
    expected = {"volume_path": volume_path, "chapters": [0, 1, 2]}

    result = update_chapter_list(volume_path, moved_files, chapters)

    assert result == expected


def test_given_a_list_of_names_and_json_organize_file_names(json_file):
    pass


def test_round_partial_chapters_to_nearest_chapter(json_file):
    pass
