from service.google_drive_api import create_service

CLIENT_SECRET_FILE = '../service/client_secret_google.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def create_folder(google_service, folder_name):
    metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    google_service.files().create(body=metadata).execute()


def create_folders(google_service, folder_names):
    for folder_name in folder_names:
        create_folder(google_service, folder_name)


