from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import yamlReader
import hoursAndWageCalculator

# If modifying these scopes, delete the file calendar.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata', 'https://www.googleapis.com/auth/drive']



def main():
    creds = hoursAndWageCalculator.getCreds('drive.pickle','drive.json')

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    try:
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        yaml = yamlReader.getYaml()
        if not items:
            print('No files found.')
        else:
            for item in items:
                if (item['name'] == yaml):
                    # get Google Drive ID for configuration file named calculator_data.yml
                    yamlID = item['id']
                    # print('{0}'.format(item['id']))
                    # download configuration file contents
                    body = service.files().get_media(fileId=yamlID).execute()
                    formattedOutput = body.decode("utf-8")
                    tmp = formattedOutput.replace('\r\n', '\n')
                    # write contents to local file
                    with open(yaml, 'w') as f:
                        print(tmp, file=f)
    except:
        print(
            """\nERROR: cannot access Google Drive to update configuration file\n\nWill instead use data from last successful update...""")


if __name__ == '__main__':
    main()
