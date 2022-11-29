from __future__ import print_function

import os
import os.path
import io
import googleapiclient.http
from storagedrive import StorageDrive
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
# Scope to see information about files in Google Drive.
SCOPES_INFORMATION = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# Scope to see and download files from Google Drive.
SCOPES_DOWNLOAD_FILES = ['https://www.googleapis.com/auth/drive.readonly']


class GoogleDrive(StorageDrive):
    creds = None

    def __init__(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES_INFORMATION)
            # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if False and self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES_INFORMATION)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    def upload(self, file_path):
        # Path to the file to upload.
        file_path = file_path
        self.__init__()
        try:
            # create drive api client
            service = build('drive', 'v3', credentials=self.creds)

            file_metadata = {'name': os.path.basename(file_path)}
            media = MediaFileUpload(file_path,
                                    mimetype='image/jpeg')
            file = service.files().create(body=file_metadata, media_body=media,
                                          fields='id').execute()
            print(F'File ID: {file.get("id")}')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

    def download(self, real_file_id):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES_DOWNLOAD_FILES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if False and creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES_DOWNLOAD_FILES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('drive', 'v3', credentials=creds)
            file_id = real_file_id

            # pylint: disable=maybe-no-member
            request = service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = googleapiclient.http.MediaIoBaseDownload(file, request, chunksize=1024*1024)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

        return file.getvalue()

    def search(self):

        self.__init__()
        try:
            # create drive api client
            service = build('drive', 'v3', credentials=self.creds)
            files = []
            page_token = None
            while True:
                # pylint: disable=maybe-no-member
                response = service.files().list(q="mimeType='image/jpeg'",
                                                spaces='drive',
                                                fields='nextPageToken, '
                                                       'files(id, name)',
                                                pageToken=page_token).execute()
                for file in response.get('files', []):
                    # Process change
                    print(F'Found file: {file.get("name")}, {file.get("id")}')
                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

        except HttpError as error:
            print(F'An error occurred: {error}')
            files = None

        return files
