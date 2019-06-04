import smtplib
import yamlReader
import GoogleApi
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main(start, end, mail):
    # fetch email server username
    username = yamlReader.getUsername()

    # fetch email server password
    password = yamlReader.getPassword()

    # fetch email recipients list
    recipients = yamlReader.getEmailRecipients()

    # initialise email server
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    # output from GoogleApi.py
    unformattedMsg = GoogleApi.main(start, end)
    # send message to all recipients from list
    try:
        for recipient in recipients:
            # create and format message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Working hours"
            msg['From'] = username
            msg['To'] = recipient
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
            formatting = MIMEText(html, 'html')
            msg.attach(formatting)
            # server.sendmail(username, recipient, msg.as_string())
            print("Email sent successfully to: " + recipient)
    except:
        print("Failed to send email! ")
    server.quit()


if __name__ == '__main__':
    main(0, 0, 0, )
