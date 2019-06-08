from __future__ import print_function
from googleapiclient.discovery import build
import yamlReader
import hoursAndWageCalculator
from base64 import urlsafe_b64encode
from apiclient import errors
from email.mime.text import MIMEText
import getGoogleCredentials


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    encoded_message = urlsafe_b64encode(message.as_string())  # .as_bytes() for python 3.7
    return {'raw': encoded_message.decode()}


def generateAndSendEmail(start, end):

    creds = getGoogleCredentials.getCreds()
    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    sender = "me"
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


if __name__ == '__main__':
    generateAndSendEmail(None, None)
