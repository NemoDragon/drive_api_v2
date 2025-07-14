import os
import io
from googleapiclient.http import MediaIoBaseDownload


def download_file(google_service, local_folder_name, file_id, file_name, mime_type):

    if mime_type == 'application/vnd.google-apps.document' or mime_type == 'application/vnd.google-apps.presentation':
        request = google_service.files().export_media(fileId=file_id, mimeType='application/pdf')
    else:
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
