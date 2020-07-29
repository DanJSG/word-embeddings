import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

class GDrive:
    def __init__(self, creds_path):
        self.scopes = ['https://www.googleapis.com/auth/drive.file']
        self.creds = self._authenticate(creds_path)
        self.service = build('drive', 'v3', credentials=self.creds)

    def upload_file(self, local_path, name, mime_type, parent_folder=None):
        upload_path = {'name': name}
        if parent_folder:
            upload_path["parents"] = [parent_folder]
        file = MediaFileUpload(local_path, mimetype=mime_type)
        # pylint: disable=maybe-no-member
        created = self.service.files().create(body=upload_path, media_body=file, fields='id').execute()
        print(created)

    def _authenticate(self, creds_path):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.scopes)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

# def main():
#     drive_service = GDrive('credentials.json')
#     drive_service.upload_file('testfile.txt', 'soupoup.txt', 'text/plain', parent_folder="1nL06sTcS3otE2BLkzPJpwBDe_ajN3rZy")

# main()
