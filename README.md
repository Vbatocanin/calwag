# Wage calculator manual

### Initial Setup

To use the calculator, proceed with the following steps:

1. Download and extract the provided zip file `wage_calculator.zip`

2. Log into any Google account that can view the work hours calendar

   > Note: The configuration file will be stored on this same account's Google Drive

3. Click the following link:

   - https://developers.google.com/drive/api/v3/quickstart/python
   - once on the site, click the `ENABLE THE DRIVE API` button, then `yes`, then `next`, then `DOWLOAD CLIENT CONFIGURATION`
   - the downloaded file will be named, `credentials.json`
   - rename  `credentials.json` to `drive.json`

4. Click the following link:

   - https://developers.google.com/calendar/quickstart/python
   - once on the site, click the `ENABLE GOOGLE CALENDAR API` button, then `yes`, then `next`, then `DOWLOAD CLIENT CONFIGURATION`
   - the downloaded file will be named, `credentials.json`
   - rename  `credentials.json` to `calendar.json`

5. Go to the Google drive on the same Google account as the one used in step `1`:

   - upload the provided the `template.yaml` provided by us, this is the template for the configuration file you can configure later

   - on Google drive, right click on `template.yaml`, select `open with`, then `connect more apps`

   - in the search bar, type in `anyfile notepad`, then using said program, `template.yaml` can be edited

   - `template.yaml` can be edited by right clicking on the file, and selecting  `anyfile notepad`, upon making appropriate changes, make sure to save them by clicking the `save` button

   - right-click on `template.yaml`, then `share`, then copy the provided link, which should look something like this:

     > https://drive.google.com/file/d/ **18Hzz__cX7K3fv_tpZmJsa620EXYwPj0d/view?usp=sharing**

   - from **your own link**, copy the emphasized text starting with `18H..` and ending with `../view` (excluding both / and view) to the provided start.py python file (there will be a clear indicator in the file itself)

     

6. Open the `template.yaml` file on your Drive, and change the `email_server_username` and `email_server_password` to the username and password of the Google Account you will be using as a server (this can, but doesn't have to be the same account from step `1`, it can be an independent account with no access to the main calendar)


7. Log onto the account that will be used to send emails from step `6`, then click the following link:
   - https://myaccount.google.com/security?pli=1
   - scroll down and turn **on** `Less secure app access`

8. Run the provided `setup.sh` file, this will automatically install all necessary packages for the wage calculator

9. Begin using the program by executing the provided `start.py` python file

   >Executing Python file on MacOS: 
   >
   >- Go to System Preferences and select Keyboard > Shortcuts > Services. Find "New Terminal at Folder"
   >- Type into the terminal: "./name_of_file.py", like for example "./start.py"
   >
   >
   >Same goes for Linux, the only difference being that you open the terminal in a specific folder by right clicking in the folder and clicking the `Open in Terminal` buttion

10. Follow the instructions in the terminal.

Programmers:

- Marko Petrovic
- Vladimir Batocanin

