import os
import webbrowser

myCmd1 = 'sudo easy_install pip'
myCmd2 = 'sudo pip install --upgrade pip'
myCmd3 = 'sudo pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib yamlreader'

os.system(myCmd1)
os.system(myCmd2)
os.system(myCmd3)

webbrowser.open_new("https://developers.google.com/calendar/quickstart/python?authuser=1")
webbrowser.open_new_tab("https://developers.google.com/drive/api/v3/quickstart/python")
webbrowser.open_new_tab("https://developers.google.com/gmail/api/quickstart/python")
