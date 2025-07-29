import os
import shutil
from pathlib import Path

class DriveHelper:
    
    def __init__(self, base_path=None, drive_type="local", gcs_client=None, drive_client=None):
        """
        drive_type: "local", "gcs", or "gdrive"
        base_path: For local or cloud storage root folder
        gcs_client: Optional GCS helper instance
        drive_client: Optional Google Drive helper instance
        """
        self.drive_type = drive_type
        self.base_path = base_path or os.getenv("CHROMA_PERSIST_PATH", "./chroma_store")
        self.gcs_client = gcs_client
        self.drive_client = drive_client

    def get_chroma_storage_path(self):
        """Returns a usable local path for Chroma persistent storage."""
        if self.drive_type == "local":
            Path(self.base_path).mkdir(parents=True, exist_ok=True)
            return self.base_path

        elif self.drive_type == "gcs":
            local_path = Path("./gcs_chroma_cache")
            local_path.mkdir(parents=True, exist_ok=True)
            self.sync_from_remote()  # Sync when requesting path
            return str(local_path)

        elif self.drive_type == "gdrive":
            local_path = Path("./gdrive_chroma_cache")
            local_path.mkdir(parents=True, exist_ok=True)
            self.sync_from_remote()
            return str(local_path)

        else:
            raise ValueError("Unsupported drive type: must be 'local', 'gcs', or 'gdrive'")

    def upload_chroma_data(self, folder_name="chroma_store"):
        if self.drive_type == "gcs" and self.gcs_client:
            bucket_name = os.getenv("GCS_BUCKET", "langxchange-data")
            for root, _, files in os.walk(self.base_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.base_path)
                    self.gcs_client.upload_file(bucket_name, file_path, f"{folder_name}/{rel_path}")

        elif self.drive_type == "gdrive" and self.drive_client:
            folder_id = self.drive_client.create_folder(folder_name)
            for root, _, files in os.walk(self.base_path):
                for f in files:
                    file_path = os.path.join(root, f)
                    self.drive_client.upload_file(file_path, parent_id=folder_id)

    def sync_from_remote(self):
        if self.drive_type == "gcs" and self.gcs_client:
            bucket_name = os.getenv("GCS_BUCKET", "langxchange-data")
            prefix = os.getenv("GCS_FOLDER", "chroma_store")
            local_dir = Path("./gcs_chroma_cache")

            blobs = self.gcs_client.list_blobs(bucket_name, prefix=prefix)
            for blob_name in blobs:
                local_path = local_dir / Path(blob_name).name
                self.gcs_client.download_file(bucket_name, blob_name, str(local_path))

        elif self.drive_type == "gdrive" and self.drive_client:
            folder_name = os.getenv("GDRIVE_FOLDER", "chroma_store")
            folder_id = self.drive_client.find_or_create_folder(folder_name)
            files = self.drive_client.list_files_in_folder(folder_id)

            local_dir = Path("./gdrive_chroma_cache")
            for f in files:
                file_id = f.get("id")
                file_name = f.get("name")
                dest_path = local_dir / file_name
                self.drive_client.download_file(file_id, str(dest_path))
