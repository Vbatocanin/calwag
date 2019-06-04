from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import yamlReader
import start


# If modifying these scopes, delete the file calendar.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata', 'https://www.googleapis.com/auth/drive']


def main():
    creds = None
    # The file calendar.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('drive.pickle'):
        with open('drive.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'drive.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('drive.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API

    # results = service.files().list(
    #    pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])

    # if not items:
    #    print('No files found.')
    # else:
    #    print('Files:')
    #    for item in items:
    #        print(u'{0} ({1})'.format(item['name'], item['id']))
    try:
        # get Google Drive ID for configuration file
        yamlID = start.yamlID()
        # download configuration file contents
        body = service.files().get_media(fileId=yamlID).execute()
        formattedOutput = body.decode("utf-8")
        tmp = formattedOutput.replace('\r\n', '\n')
        # write contents to local file
        yaml = yamlReader.getYaml()
        with open(yaml, 'w') as f:
            print(tmp, file=f)
    except:
        print(
            """\nERROR: cannot access Google Drive to update configuration file\n\nWill instead use data from last successful update...""")


if __name__ == '__main__':
    main()
