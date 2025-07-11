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
