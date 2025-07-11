def get_or_create_folder(google_service, folder_name):
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    response = google_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])
    if files:
        return files[0]['id']
    else:
        metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = google_service.files().create(body=metadata, fields='id').execute()
        return folder.get('id')


def get_or_create_folders(google_service, folder_names):
    for folder_name in folder_names:
        get_or_create_folder(google_service, folder_name)


