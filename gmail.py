from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import yamlReader
import hoursAndWageCalculator
from base64 import urlsafe_b64encode
from apiclient import errors
from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    encoded_message = urlsafe_b64encode(message.as_bytes())
    return {'raw': encoded_message.decode()}

def getCreds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('gmail.pickle'):
        with open('gmail.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gmail.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('gmail.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def generateAndSendEmail(start, end):

    creds = getCreds()
    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    sender = yamlReader.getSender()
    recipients = yamlReader.getEmailRecipients()
    unformattedMsg = hoursAndWageCalculator.getHoursAndWages(start, end)

    # create and format message
    html = """
    <html>
      <head></head>
      <body>
        <table border="1">
        %s
        </table>
      </body>
    </html>
    """ % unformattedMsg
    try:
        for recipient in recipients:
            finalMessage = create_message(sender, recipient, "Working hours", html)
            service.users().messages().send(userId="me", body=finalMessage).execute()
            print("Email sent successfully to: " + recipient)
    except errors.HttpError:
        print("Failed to send email! ")