import os
import uuid
from pathlib import Path
from langxchange.google_cs_helper import GoogleCloudStorageHelper


def test_gcs_basic_lifecycle(tmp_path):
    # Required environment variables
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "creds/crypto-lexicon-212720-a0f6d3407cb2.json")
    os.environ["GCP_PROJECT_ID"] = os.getenv("GCP_PROJECT_ID", "crypto-lexicon-212720")
    os.environ["GCS_BUCKET"] = os.getenv("GCS_BUCKET", "ikolilu_main_storage")

    credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    bucket_name = os.environ["GCS_BUCKET"]
    assert os.path.exists(credentials), "❌ GOOGLE_APPLICATION_CREDENTIALS file not found"
    assert bucket_name, "❌ GCS_BUCKET environment variable not set"

    # Instantiate helper
    gcs = GoogleCloudStorageHelper()
    blob_name = f"test_{uuid.uuid4().hex}.txt"

    # Create a sample file
    file_path = tmp_path / "sample.txt"
    content = "Hello from LangXchange test!"
    file_path.write_text(content)

    # Upload
    assert gcs.upload_file(bucket_name, str(file_path), blob_name)

    # List
    blobs = gcs.list_blobs(bucket_name)
    assert blob_name in blobs

    # Download
    download_path = tmp_path / "downloaded.txt"
    assert gcs.download_file(bucket_name, blob_name, str(download_path))
    assert download_path.read_text() == content

    # Delete
    assert gcs.delete_blob(bucket_name, blob_name)
    print(f"✅ Test passed for blob: {blob_name}")

# import os
# import uuid
# from pathlib import Path
# from langxchange.google_cs_helper import GoogleCloudStorageHelper


# def test_gcs_full_lifecycle(tmp_path):
#     # --- Set required environment variables ---
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "creds/crypto-lexicon-212720-a0f6d3407cb2.json")
#     os.environ["GCP_PROJECT_ID"] = os.getenv("GCP_PROJECT_ID", "crypto-lexicon-212720")
#     os.environ["GCS_BUCKET"] = os.getenv("GCS_BUCKET", "ikolilu_main_storage")

#     # --- Validate setup ---
#     credentials_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
#     project_id = os.environ["GCP_PROJECT_ID"]
#     bucket_name = os.environ["GCS_BUCKET"]

#     assert os.path.exists(credentials_path), "❌ GOOGLE_APPLICATION_CREDENTIALS file not found"
#     assert project_id, "❌ GCP_PROJECT_ID is not set"
#     assert bucket_name, "❌ GCS_BUCKET is not set"

#     # --- Setup sample file ---
#     content = "🌍 Hello from GCS test!"
#     sample_file = tmp_path / "hello.txt"
#     sample_file.write_text(content)

#     helper = GoogleCloudStorageHelper()
#     blob_name = f"test_upload_{uuid.uuid4().hex}.txt"

#     # --- Upload ---
#     assert helper.upload_file(bucket_name, str(sample_file), blob_name)

#     # --- List ---
#     blobs = helper.list_blobs(bucket_name)
#     assert blob_name in blobs

#     # --- Download ---
#     download_path = tmp_path / "downloaded.txt"
#     assert helper.download_file(bucket_name, blob_name, str(download_path))
#     assert download_path.read_text() == content

#     # --- Delete ---
#     assert helper.delete_blob(bucket_name, blob_name)

#     print(f"✅ GCS lifecycle test passed for blob: {blob_name}")
