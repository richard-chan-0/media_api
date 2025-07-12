import pytest
from unittest.mock import patch, MagicMock
from src.services.manage_media.create_volumes import create_volumes
from src.lib.dataclasses import ServiceArguments


@pytest.fixture
def mock_args():
    return ServiceArguments(
        story="Test Story",
        directory_in="/fake/input",
        volume_mapping={"vol1": ["ch1", "ch2"], "vol2": ["ch3"]},
    )


@patch("src.services.manage_media.create_volumes.create_volume_directories")
@patch("src.services.manage_media.create_volumes.create_volume")
def test_create_volumes_calls_create_volume_for_each_folder(
    mock_create_volume, mock_create_volume_directories, mock_args
):
    # Arrange
    folder1 = MagicMock()
    folder1.name = "vol1-folder"
    folder1.path = "/fake/input/vol1-folder"
    folder2 = MagicMock()
    folder2.name = "vol2-folder"
    folder2.path = "/fake/input/vol2-folder"
    mock_create_volume_directories.return_value = [folder1, folder2]

    # Act
    create_volumes(mock_args)

    # Assert
    assert mock_create_volume.call_count == 2
    mock_create_volume.assert_any_call(
        mock_args.directory_in,
        folder1.path,
        volume_name="vol1",
        ignore_files=[],
    )
    mock_create_volume.assert_any_call(
        mock_args.directory_in,
        folder2.path,
        volume_name="vol2",
        ignore_files=[],
    )


@patch("src.services.manage_media.create_volumes.create_volume_directories")
@patch("src.services.manage_media.create_volumes.create_volume")
def test_create_volumes_handles_no_folders(
    mock_create_volume, mock_create_volume_directories, mock_args
):
    mock_create_volume_directories.return_value = []
    create_volumes(mock_args)
    mock_create_volume.assert_not_called()
