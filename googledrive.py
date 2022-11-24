#!/usr/bin/python
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Google Drive Quickstart in Python.

This script uploads a single file to Google Drive.
"""

from __future__ import print_function

import os
import os.path
import io
import six
import googleapiclient.http
import httplib2
import oauth2client.client
from storagedrive import StorageDrive
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# If modifying these scopes, delete the file token.json.
SCOPES1 = ['https://www.googleapis.com/auth/drive.readonly']


class GoogleDrive(StorageDrive):

    def upload(self, file_name):

        # OAuth 2.0 scope that will be authorized.
        # Check https://developers.google.com/drive/scopes for all available scopes.
        OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'
        # Location of the client secrets.
        CLIENT_SECRETS = 'credentials.json'
        # Path to the file to upload.
        FILENAME = file_name
        # Metadata about the file.
        MIMETYPE = 'text/plain'
        TITLE = os.path.basename(file_name)
        DESCRIPTION = f'A text document about {Path(file_name).stem}.'
        # Perform OAuth2.0 authorization flow.
        flow = oauth2client.client.flow_from_clientsecrets(
            CLIENT_SECRETS, OAUTH2_SCOPE)
        flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
        authorize_url = flow.step1_get_authorize_url()
        print('Go to the following link in your browser: ' + authorize_url)
        # `six` library supports Python2 and Python3 without redefining builtin input()
        code = six.moves.input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)
        # Create an authorized Drive API client.
        http = httplib2.Http()
        credentials.authorize(http)
        drive_service = build('drive', 'v2', http=http)
        # Insert a file. Files are comprised of contents and metadata.
        # MediaFileUpload abstracts uploading file contents from a file on disk.
        media_body = googleapiclient.http.MediaFileUpload(
            FILENAME,
            mimetype=MIMETYPE,
            resumable=True
        )
        # The body contains the metadata for the file.
        body = {
            'title': TITLE,
            'description': DESCRIPTION,
        }
        # Perform the request and print the result.
        try:
            new_file = drive_service.files().insert(
                body=body, media_body=media_body).execute()
            file_title = new_file.get('title')
            file_desc = new_file.get('description')
            if file_title == TITLE and file_desc == DESCRIPTION:
                print(f"File is uploaded \nTitle : {file_title}  \nDescription : {file_desc}")
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    def download(self, real_file_id):

        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES1)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if False and creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES1)
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

    if __name__ == '__main__':
        download(real_file_id='1FEu2J_quHbg2nyUYUhuxyI9AZyKARTsM')

    def search(self):
        """Search file in drive location

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if False and creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # create drive api client
            service = build('drive', 'v3', credentials=creds)
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

    if __name__ == '__main__':
        search()
