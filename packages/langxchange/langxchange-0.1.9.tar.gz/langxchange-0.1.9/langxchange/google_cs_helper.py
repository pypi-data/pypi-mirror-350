import os
from google.cloud import storage
from google.oauth2 import service_account
from pathlib import Path

class GoogleCloudStorageHelper:
    def __init__(self, credentials_path=None):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        credentials_path = credentials_path or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if credentials_path and os.path.isfile(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = storage.Client(project=self.project_id, credentials=credentials)
        else:
            # Use ADC if credentials file not explicitly provided
            self.client = storage.Client(project=self.project_id)

    def create_bucket(self, bucket_name):
        try:
            bucket = self.client.bucket(bucket_name)
            if not bucket.exists():
                bucket = self.client.create_bucket(bucket_name)
            return bucket
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to create bucket: {e}")

    def upload_file(self, bucket_name, file_path, destination_blob_name=None):
        if not destination_blob_name:
            destination_blob_name = os.path.basename(file_path)
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(file_path)
            return True
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to upload file: {e}")

    def download_file(self, bucket_name, blob_name, destination_file_path):
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            Path(destination_file_path).parent.mkdir(parents=True, exist_ok=True)
            blob.download_to_filename(destination_file_path)
            return True
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to download file: {e}")

    def list_blobs(self, bucket_name, prefix=None):
        try:
            blobs = self.client.list_blobs(bucket_name, prefix=prefix)
            return [blob.name for blob in blobs]
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to list blobs: {e}")

    def delete_blob(self, bucket_name, blob_name):
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
            return True
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to delete blob: {e}")
