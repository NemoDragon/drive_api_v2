import os
import io
from google_drive_api import create_service
from download_files import download_file
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd

CLIENT_SECRET_FILE = 'client_secret_google.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


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
                download_file(google_service, 'data', file['id'], file['name'])
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
