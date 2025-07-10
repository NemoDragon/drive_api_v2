import os
import io
from google_drive_api import create_service
from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRET_FILE = 'client_secret_google.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_ids = ['1V8mki3KF-m6fCKGPy6xfHkHb3MiwUGmB', '1Qmp5HsB4TVMqytzaFNGO00NLCQaplvdY']
file_names = ['track1.pdf', 'track2.pdf']


def download_file(google_service, local_folder_name, file_id, file_name):
    request = google_service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done = False

    while not done:
        status, done = downloader.next_chunk()
        print('Download progress {0}'.format(status.progress() * 100))

    fh.seek(0)

    with open(os.path.join(f'./{local_folder_name}', file_name), 'wb') as f:
        f.write(fh.read())
        f.close()


for file_id, file_name in zip(file_ids, file_names):
    download_file(service, 'data', file_id, file_name)




