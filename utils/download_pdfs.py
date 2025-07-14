import os
import io
from utils.download_files import download_file
from utils.upload_files import upload_file
from utils.create_folders import get_or_create_folder
from googleapiclient.http import MediaIoBaseDownload
import hashlib


def file_hash(filepath):
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def remote_file_hash(google_service, file_id):
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


def download_all_files_recursive(google_service, folder_id, file_types,  parent_path=''):
    target_folder_id = get_or_create_folder(google_service, 'files_for_notebookLM')
    os.makedirs('data', exist_ok=True)

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
            print('in folder: ', parent_path)
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                subfolder_path = f"{parent_path}/{file['name']}"
                all_files.extend(download_all_files_recursive(google_service, file['id'], file_types, subfolder_path))
            elif file['mimeType'] in file_types:
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
