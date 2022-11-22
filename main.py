from googledrive import GoogleDrive

file = input("Enter file path: ")
driver = GoogleDrive()
driver.upload(file)






'''
from __future__ import print_function

from Google import Create_Service


CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
print(dir(service))
'''