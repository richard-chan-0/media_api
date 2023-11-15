import src.rename_media.name_functions as NameFunctions


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
