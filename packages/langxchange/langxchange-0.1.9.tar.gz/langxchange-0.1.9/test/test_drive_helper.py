import os
import shutil
import pytest
from pathlib import Path
from langxchange.drive_helper import DriveHelper


@pytest.fixture
def local_test_dir(tmp_path):
    test_path = tmp_path / "local_chroma"
    os.environ["CHROMA_PERSIST_PATH"] = str(test_path)
    return str(test_path)


def test_local_storage_path_creation(local_test_dir):
    helper = DriveHelper(drive_type="local")
    path = helper.get_chroma_storage_path()
    assert os.path.exists(path)
    assert os.path.isdir(path)


def test_invalid_drive_type():
    with pytest.raises(ValueError):
        DriveHelper(drive_type="invalid").get_chroma_storage_path()


def test_gcs_sync_from_remote_mock(monkeypatch, tmp_path):
    class MockGCS:
        def list_blobs(self, bucket, prefix):
            return ["chroma_store/file1.txt"]

        def download_file(self, bucket, blob_name, destination):
            Path(destination).write_text("sample content")

    monkeypatch.setenv("GCS_BUCKET", "mock-bucket")
    monkeypatch.setenv("GCS_FOLDER", "chroma_store")

    helper = DriveHelper(drive_type="gcs", gcs_client=MockGCS())
    path = helper.get_chroma_storage_path()
    expected_file = Path(path) / "file1.txt"
    assert expected_file.exists()
    assert expected_file.read_text() == "sample content"


def test_gdrive_sync_from_remote_mock(monkeypatch, tmp_path):
    class MockDrive:
        def find_or_create_folder(self, name):
            return "folder123"

        def list_files_in_folder(self, folder_id):
            return [{"id": "file1", "name": "sync.txt"}]

        def download_file(self, file_id, destination):
            Path(destination).write_text("drive content")

    monkeypatch.setenv("GDRIVE_FOLDER", "chroma_store")

    helper = DriveHelper(drive_type="gdrive", drive_client=MockDrive())
    path = helper.get_chroma_storage_path()
    expected_file = Path(path) / "sync.txt"
    assert expected_file.exists()
    assert expected_file.read_text() == "drive content"
