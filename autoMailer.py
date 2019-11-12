from __future__ import print_function

import datetime

from googleapiclient.discovery import build
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
import getGoogleCredentials
import hoursAndWageCalculator
import dateFunctions
import yamlReader


def handleError(temp_dict, service, recipients, user_id, msg_id, errorMsg):
    sender = temp_dict['Sender'][temp_dict['Sender'].find("<") + 1:temp_dict['Sender'].find(">")]
    recipients.append(sender)
    recipients = list(dict.fromkeys(recipients))

    # in case of error, return an email informing the user an error occured, and label the faulty email as read
    defaultDay = yamlReader.getDefault()
    if errorMsg is None:
        errorMsg = "An error occured, this is most often caused by incorrectly formatting the inputed dates."
        print("Error: ", errorMsg)
    else:
        print("Error: ", errorMsg)
    html = """
                              <html>
                                <head></head>
                                <body>
                                  %s
                                </body>
                              </html>
                              <h2>CalWag instructions:</h2>
                              <p>1. Your email must have the subject "<strong>Calwag</strong>" to get a response.</p>
                              <p>2. Write dates in this format: <strong>dd.mm.yyyy</strong></p>
                              <p>3. You can choose to send <strong>a blank email</strong> or <strong>2</strong> dates:</p>
                              <p>&nbsp; &nbsp; <strong>a blank email:</strong> will return wages from the """ % errorMsg + defaultDay.__str__() + """ two months ago until the """ + defaultDay.__str__() + """ of the following month. (Sending a blank email will get you wages from <strong>10.8.2019</strong> to <strong>9.9.2019</strong>)</p>
                              <p>&nbsp; &nbsp; <strong>2 dates:</strong> will return the wages between those 2 dates (the dates must be&nbsp;separated by a space, example: <strong>21.3.2019 31.3.2019</strong>)</p>
                              <p>4. To edit the calculator data click <a href="https://drive.google.com/open?id=1_GYHPCA1qwEehpspIHtvaRomw_fkpBzq">here</a>, and choose Anyfile Notepad to open the file.</p></p>
                              """
    for recipient in recipients:
        finalMessage = create_message("me", recipient,
                                      "Error", html)
        service.users().messages().send(userId="me", body=finalMessage).execute()
    service.users().messages().modify(userId=user_id, id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()


def main():
    try:
        creds = getGoogleCredentials.getCreds()
        service = build('gmail', 'v1', credentials=creds)
        messages = ListMessagesMatchingQuery(service, 'me')
        for message in messages:
            GetMessage(service, 'me', message['id'])
    except:
        print("Error loading gmail api/getting messages!")
        pass


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
        print("Error while listing unread messages")


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
    errorInd = 0
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
        yamlReader.refresh()
        words = temp_dict['Snippet'].split()
        start = None
        end = None
        if (words != []):
            try:
                if CheckDate(words[0]):
                    start = words[0]
                else:
                    errorInd = 1
            except:
                pass

            try:
                if CheckDate(words[1]):
                    end = words[1]
                else:
                    errorInd = 1
            except:
                pass

        sender = temp_dict['Sender'][temp_dict['Sender'].find("<") + 1:temp_dict['Sender'].find(">")]
        recipients.append(sender)
        recipients = list(dict.fromkeys(recipients))

        try:
            if errorInd == 1:
                raise ValueError("Wrong format")

            msgEmail, msgPrint, beginTime, endTime = hoursAndWageCalculator.getHoursAndWages(start, end)
            print("Begin time: ", beginTime)
            print("End time: ", endTime)

            # if a blank email is received, we append the last month's wages on top of the existing msg
            if (start is None and end is None):
                tmpEndExtraTime = endTime.day.__str__() + "." + beginTime.month.__str__() + "." + beginTime.year.__str__()
                [extraEndMonth, extraEndYear] = dateFunctions.dateLastMonth(beginTime.month, beginTime.year)
                tmpBeginExtraTime = beginTime.day.__str__() + "." + extraEndMonth.__str__() + "." + extraEndYear.__str__()

                msgEmailExtra, msgPrintExtra, beginTimeExtra, endTimeExtra = hoursAndWageCalculator.getHoursAndWages(
                    tmpBeginExtraTime, tmpEndExtraTime)
                msgEmail = msgEmail + msgEmailExtra

            defaultDay = yamlReader.getDefault()
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
            <p>&nbsp; &nbsp; <strong>a blank email:</strong> will return wages from the """ % msgEmail + defaultDay.__str__() + """ a months ago until the """ + defaultDay.__str__() + """ of the following month, followed 
            by wages from the """ + defaultDay.__str__() + """ two months ago until the """ + defaultDay.__str__() + """ of the last month.</p>
            <p>&nbsp; &nbsp; <strong>2 dates:</strong> will return the wages between those 2 dates (the dates must be&nbsp;separated by a space, example: <strong>21.3.2019 31.3.2019</strong>)</p>
            <p>4. To edit the calculator data click <a href="https://drive.google.com/open?id=1_GYHPCA1qwEehpspIHtvaRomw_fkpBzq">here</a>, and choose Anyfile Notepad to open the file.</p></p>
            """

            # final msg formatting
            tempStartDay = beginTime.day
            tempStartMonth = beginTime.month
            tempStartYear = beginTime.year
            tempEndDay = endTime.day
            tempEndMonth = endTime.month
            tempEndYear = endTime.year
            print("Wages calculated at ", datetime.datetime.now())
            for recipient in recipients:
                finalMessage = create_message("me", recipient,
                                              "CalWag: " + str(tempStartDay) + "." + str(tempStartMonth) + "." + str(
                                                  tempStartYear) + " - " + str(tempEndDay) + "." + str(
                                                  tempEndMonth) + "." + str(tempEndYear), html)
                service.users().messages().send(userId="me", body=finalMessage).execute()
                print("Email sent successfully to: " + recipient)
                print("##########################################")
            service.users().messages().modify(userId=user_id, id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

        except Exception:
            handleError(temp_dict, service, recipients, user_id, msg_id,
                        "Error: invalid date or wrong date format, must be dd.mm.yyyy")
    else:
        handleError(temp_dict, service, recipients, user_id, msg_id, "Error: subject of email must be calwag")


if __name__ == '__main__':
    main()
