from __future__ import print_function
from googleapiclient.discovery import build
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
import getGoogleCredentials
import hoursAndWageCalculator


def main():
    creds = getGoogleCredentials.getCreds()
    service = build('gmail', 'v1', credentials=creds)
    messages = ListMessagesMatchingQuery(service, 'me')
    for message in messages:
        GetMessage(service, 'me', message['id'])


def CheckDate(date):
    numbers = date.split(".")
    if 0 < int(numbers[0]) < 32 and 0 < int(numbers[1]) < 13 and 2000 < int(numbers[2]) < 2100:
        return True
    else:
        return False


def ListMessagesMatchingQuery(service, user_id):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=100).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, pageToken=page_token).execute()
      messages.extend(response['messages'])
    return messages
  except:
    print("error")


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    encoded_message = urlsafe_b64encode(message.as_bytes())  # .as_bytes() for python 3.7, .as_string() for python 2.7
    return {'raw': encoded_message.decode()}


def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.


  Returns:
    A Message.
  """
  try:
    temp_dict = {}
    recipients = []
    message = service.users().messages().get(userId=user_id, id=msg_id, format="full", metadataHeaders=None).execute()
    headers = message["payload"]["headers"]
    subject = [i['value'] for i in headers if i["name"] == "Subject"]

    for three in headers:
        if three['name'] == 'From':
            msg_from = three['value']
            temp_dict['Sender'] = msg_from
        else:
            pass

    temp_dict['Snippet'] = message['snippet']

    if subject[0].upper().strip() == 'CALWAG':
        words = temp_dict['Snippet'].split()
        start = None
        end = None

        try:
            if CheckDate(words[0]):
               start = words[0]
            else:
               start = None
        except:
            pass

        try:
            if CheckDate(words[1]):
                end = words[1]
            else:
                end = None
        except:
            pass

        sender = temp_dict['Sender'][temp_dict['Sender'].find("<")+1:temp_dict['Sender'].find(">")]
        recipients.append(sender)
        recipients = list(dict.fromkeys(recipients))
        msgEmail, msgPrint, beginTime, endTime = hoursAndWageCalculator.getHoursAndWages(start, end)

        html = """
            <html>
              <head></head>
              <body>
                <table border="1">
                %s
                </table>
              </body>
            </html>
            <h2>CalWag instructions:</h2>
            <p>1. Your email must have the subject "<strong>Calwag</strong>" to get a response.</p>
            <p>2. Write dates in this format: <strong>dd.mm.yyyy</strong></p>
            <p>3. You can choose to send <strong>a blank email</strong> or <strong>2</strong> dates:</p>
            <p>&nbsp; &nbsp; <strong>a blank email:</strong> will return wages from the 10. two months ago until the 10. of the following month. (Sending a blank email will get you wages from <strong>10.8.2019</strong> to <strong>9.9.2019</strong>)</p>
            <p>&nbsp; &nbsp; <strong>2 dates:</strong> will return the wages between those 2 dates (the dates must be&nbsp;separated by a space, example: <strong>21.3.2019 31.3.2019</strong>)</p>
            </p>
            """ % msgEmail

        tempStartDay = beginTime.day
        tempStartMonth = beginTime.month
        tempStartYear = beginTime.year
        tempEndDay = endTime.day
        tempEndMonth = endTime.month
        tempEndYear = endTime.year
        for recipient in recipients:
            finalMessage = create_message("me", recipient, "CalWag: " + str(tempStartDay) + "." + str(tempStartMonth) + "." + str(tempStartYear) + " - " + str(tempEndDay) + "." + str(tempEndMonth) + "." + str(tempEndYear), html)
            service.users().messages().send(userId="me", body=finalMessage).execute()
            print("Email sent successfully to: " + recipient)
    service.users().messages().modify(userId=user_id, id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
  except:
    print('error')
    service.users().messages().modify(userId=user_id, id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()


if __name__ == '__main__':
    main()
