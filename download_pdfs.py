import os
import io
from google_drive_api import create_service
from download_files import download_file
from upload_files import upload_file
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd
import hashlib

CLIENT_SECRET_FILE = 'client_secret_google.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
target_folder_id = '1AY8HjaXAj1jy2Bl5rY3dHB7rDMlYZOcz'


def file_hash(filepath):
    """Hash lokalnego pliku."""
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def remote_file_hash(google_service, file_id):
    """Hash pliku PDF z Google Drive (nie zapisuje na dysk)."""
    hasher = hashlib.md5()
    request = google_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    for chunk in iter(lambda: fh.read(4096), b""):
        hasher.update(chunk)
    return hasher.hexdigest()


def download_all_pdfs_recursive(google_service, folder_id, parent_path=''):
    all_files = []
    page_token = None

    while True:
        query = f"'{folder_id}' in parents and trashed = false"
        response = google_service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token
        ).execute()

        for file in response.get('files', []):
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                subfolder_path = f"{parent_path}/{file['name']}"
                all_files.extend(download_all_pdfs_recursive(google_service, file['id'], subfolder_path))
            elif file['mimeType'] == 'application/pdf':
                file['folder_path'] = parent_path
                local_folder = 'data'
                local_path = os.path.join(local_folder, file['name'])

                local_hash = file_hash(local_path)
                remote_hash = remote_file_hash(google_service, file['id'])

                if local_hash != remote_hash:
                    print(f"Download or update: {file['name']}")
                    download_file(google_service, local_folder, file['id'], file['name'])
                    upload_file(google_service, target_folder_id, local_folder, file['name'], file['mimeType'])
                else:
                    print(f"File is up to date: {file['name']}")
                all_files.append(file)

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    return all_files


main_folder_id = '17mlh6KoSQlOlIWyFeQH_j30eNxLLH2sP'
files = download_all_pdfs_recursive(service, main_folder_id, parent_path='')
print(files)

df = pd.DataFrame(files)
print(df)
