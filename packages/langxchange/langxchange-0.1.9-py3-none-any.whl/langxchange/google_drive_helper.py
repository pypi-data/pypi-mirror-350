import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle


class GoogleDriveHelper:
    def __init__(self, credentials_path="credentials.json", token_path="token.pickle"):
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.creds = None
        self.token_path = token_path

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.scopes)
                self.creds = flow.run_local_server(port=0)
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('drive', 'v3', credentials=self.creds)

    def create_folder(self, name, parent_id=None):
        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            metadata['parents'] = [parent_id]

        folder = self.service.files().create(body=metadata, fields='id').execute()
        return folder.get('id')

    def upload_file(self, file_path, parent_id=None, mime_type=None):
        file_metadata = {'name': os.path.basename(file_path)}
        if parent_id:
            file_metadata['parents'] = [parent_id]
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')

    def list_files_in_folder(self, folder_id):
        query = f"'{folder_id}' in parents and trashed = false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        return results.get('files', [])

    def read_file_content(self, file_id):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)
        return fh.read().decode()

    def download_file(self, file_id, output_path):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(output_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
        fh.close()

    def get_file_metadata(self, file_id):
        return self.service.files().get(fileId=file_id, fields='id, name, mimeType, parents').execute()

    def delete_file(self, file_id):
        self.service.files().delete(fileId=file_id).execute()

    def rename_file(self, file_id, new_name):
        file_metadata = {'name': new_name}
        updated_file = self.service.files().update(fileId=file_id, body=file_metadata).execute()
        return updated_file.get('name')
