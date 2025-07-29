import os
import time
import pytest
from pathlib import Path
from langxchange.gcs_helper import GoogleCloudStorageHelper


@pytest.fixture(scope="module", autouse=True)
def setenv():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(Path("credentials.json").resolve())
    os.environ["GCP_PROJECT_ID"] = "your-gcp-project-id"  # TODO: Replace with your actual project ID


@pytest.fixture(scope="module")
def gcs():
    return GoogleCloudStorageHelper(project_id=os.getenv("GCP_PROJECT_ID"))


@pytest.fixture(scope="module")
def test_bucket_name(gcs):
    timestamp = int(time.time())
    bucket_name = f"langxchange-test-{timestamp}"
    gcs.create_bucket(bucket_name)
    yield bucket_name
    gcs.delete_bucket(bucket_name)


@pytest.fixture
def test_file(tmp_path):
    file = tmp_path / "test_upload.txt"
    file.write_text("Hello from LangXchange test!")
    return file


def test_upload_and_list_blob(gcs, test_bucket_name, test_file):
    uri = gcs.upload_file(test_bucket_name, str(test_file))
    assert uri.startswith("gs://")

    blobs = gcs.list_blobs(test_bucket_name)
    assert "test_upload.txt" in blobs


def test_read_blob(gcs, test_bucket_name):
    content = gcs.read_blob(test_bucket_name, "test_upload.txt")
    assert "LangXchange" in content


def test_download_blob(gcs, test_bucket_name, tmp_path):
    local_file = tmp_path / "downloaded.txt"
    gcs.download_file(test_bucket_name, "test_upload.txt", str(local_file))
    assert local_file.exists()
    assert "LangXchange" in local_file.read_text()


def test_delete_blob(gcs, test_bucket_name):
    msg = gcs.delete_blob(test_bucket_name, "test_upload.txt")
    assert "Deleted" in msg

    blobs = gcs.list_blobs(test_bucket_name)
    assert "test_upload.txt" not in blobs
