import os

# enable safari automatization
cmd0 = 'sudo safaridriver --enable'
# install pip and the needed libraries
cmd1 = 'sudo easy_install pip'
cmd2 = 'sudo pip install --upgrade pip'
cmd3 = 'sudo pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib yamlreader selenium'
# run autocred.py to get credentials
cmd4 = 'python autocred.py'

os.system(cmd0)
os.system(cmd1)
os.system(cmd2)
os.system(cmd3)
os.system(cmd4)
