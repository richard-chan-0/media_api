from pytest import fixture
from src.organize_chapters_to_vol.organize_chapters_to_vol import (
    organize_chapters_to_vol,
)


@fixture
def json_file():
    return {
        "story": "title",
        "volumes": [
            {"volume": 1, "chapters": [1, 2, 3]},
            {"volume": 2, "chapters": [4, 5, 6]},
        ],
    }


def test_given_a_list_of_names_and_json_organize_file_names(json_file):
    # TODO: create mocks

    chapters = [
        "Bungou Stray Dogs CH - 001 @Manga_Gallery.cbz",
        "Bungou Stray Dogs CH - 002 @Manga_Gallery.cbz",
        "Bungou Stray Dogs CH - 003 @Manga_Gallery.cbz",
        "Bungou Stray Dogs CH - 004 @Manga_Gallery.cbz",
        "Bungou Stray Dogs CH - 005 @Manga_Gallery.cbz",
    ]

    expected_organization = [
        {
            "volume": 1,
            "chapters": [
                "Bungou Stray Dogs CH - 001 @Manga_Gallery.cbz",
                "Bungou Stray Dogs CH - 002 @Manga_Gallery.cbz",
                "Bungou Stray Dogs CH - 003 @Manga_Gallery.cbz",
            ],
        },
        {
            "volume": 2,
            "chapters": [
                "Bungou Stray Dogs CH - 004 @Manga_Gallery.cbz",
                "Bungou Stray Dogs CH - 005 @Manga_Gallery.cbz",
            ],
        },
    ]

    result = organize_chapters_to_vol("", "")

    assert result == expected_organization


def test_round_partial_chapters_to_nearest_chapter(json_file):
    pass
