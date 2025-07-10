from googleapiclient.http import MediaFileUpload
from google_drive_api import create_service

CLIENT_SECRET_FILE = 'client_secret_google.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

folder_id = '17mlh6KoSQlOlIWyFeQH_j30eNxLLH2sP'
file_names = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'notice.docx', 'pres.pptx', 'data1.xlsx']
mime_types = ['application/pdf', 'application/pdf', 'application/pdf',
              'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
              'application/vnd.openxmlformats-officedocument.presentationml.presentation',
              'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']

for file_name, mime_type in zip(file_names, mime_types):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload('./data/{0}'.format(file_name), mimetype=mime_type)

    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()


