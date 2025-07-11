from googleapiclient.http import MediaFileUpload


def upload_file(google_service, folder_id, local_folder_name, file_name, file_type):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(f'./{local_folder_name}/{file_name}', mimetype=file_type)

    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    response = google_service.files().list(q=query, fields="files(id)").execute()
    files = response.get('files', [])

    if files:
        file_id = files[0]['id']
        google_service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
    else:
        google_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

