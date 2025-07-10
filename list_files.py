from google_drive_api import create_service
import pandas as pd

CLIENT_SECRET_FILE = 'client_secret_google.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def list_all_files_recursive(google_service, main_folder_id, parent_path=''):
    all_files = []
    page_token = None

    while True:
        query = f"'{main_folder_id}' in parents and trashed = false"
        response = google_service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token
        ).execute()

        for file in response.get('files', []):
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                subfolder_path = f"{parent_path}/{file['name']}"
                all_files.extend(list_all_files_recursive(google_service, file['id'], subfolder_path))
            else:
                file['folder_path'] = parent_path
                all_files.append(file)

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    return all_files


folder_id = '17mlh6KoSQlOlIWyFeQH_j30eNxLLH2sP'
files = list_all_files_recursive(service, folder_id, parent_path='')
print(files)


df = pd.DataFrame(files)
print(df)
