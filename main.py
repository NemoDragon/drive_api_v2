import sys
import pandas as pd
from service.google_drive_api import create_service
from utils.download_pdfs import download_all_files_recursive


CLIENT_SECRET_FILE = 'client_secret_google.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def main():
    main_folder_id = sys.argv[1]
    file_types = ['application/pdf',
                  'application/vnd.google-apps.document',
                  'application/vnd.google-apps.presentation']

    all_files = download_all_files_recursive(service, main_folder_id, file_types, parent_path='')

    df = pd.DataFrame(all_files)
    print(df)


if __name__ == '__main__':
    main()