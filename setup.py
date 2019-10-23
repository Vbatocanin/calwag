import os

# enable safari automatization
cmd0 = 'sudo safaridriver --enable'
# install pip and the needed libraries
cmd1 = 'sudo easy_install pip'
cmd2 = 'sudo pip install --upgrade pip'
cmd3 = 'sudo pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib yamlreader selenium'


os.system(cmd0)
os.system(cmd1)
os.system(cmd2)
os.system(cmd3)
