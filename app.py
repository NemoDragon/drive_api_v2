import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

# If modifying these scopes, delete the file token.json.
# 'https://www.googleapis.com/auth/drive.metadata.readonly' allows read-only access to file metadata.
# 'https://www.googleapis.com/auth/drive' allows full access to files in Google Drive.
SCOPES = ['https://www.googleapis.com/auth/drive'] # You can use a more restrictive scope if needed, e.g., 'https://www.googleapis.com/auth/drive.readonly'

def get_drive_service():
    """Authenticates and returns the Google Drive API service."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

# Get the service object once for reuse
service = get_drive_service()

if not service:
    print("Failed to get Google Drive service. Exiting.")
    exit()