from google_drive_api import create_service

CLIENT_SECRET_FILE = 'client_secret_google.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

folder_names = ['Games', 'Games2']

for folder_name in folder_names:
    metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    service.files().create(body=metadata).execute()

