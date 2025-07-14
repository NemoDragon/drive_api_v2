# Drive API in Python for NotebookLM Task
## 1.	Description
The aim of this task is to get all files from the google drive folder and add them as the sources for the LLM model in NotebookLM. The python script will also check if any files were updated. 

## 2.	Project structure:
-	service
    -	google_drive_api.py (authentication and authorisation)
-	utils
    -	list_files.py (iterate all files)
    -	download_files.py (download file from google drive)
    -	upload_files.py (upload file to google drive)
    -	create_folders.py (create folder/folders in google drive)
    -	file_service.py (for managing pdfs, docs and slides, it downloads files from google drive folder, put them into “data” folder that is created locally and uploads them on google drive into one folder “files_for_notebookLM”)
-	client_secret_google.json (necessary file for authorisation)
-	main.py
## 3.	Instructions
### 3.1.	Create OAuth consent screen - download json, name it  “client_secret_google.json” and put it in the project’s folder
### 3.2.	Install libraries from requirements.txt:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 3.3.	Run the program: 
```
python main.py [folder_id_of_google_drive]
```

## 4.	Necessary tools for the project:
-	Google Drive API (GCP) - to iterate through Google Drive folders, download files
-	GCP project - to use Google Drive API
-	Python 3.11+
-	Google account
-	NotebookLM API: Gemini answer: There isn't a public API for directly adding sources from a device to Google NotebookLM. Solution: add all pdfs manually, but they are already grouped/updated by the script.
