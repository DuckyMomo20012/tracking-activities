from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

# For using listdir()
import os
# For get current today
from datetime import date
gauth = GoogleAuth()

# Get current dir to check if "mycreds.txt" exist:
cur_dir = os.getcwd()
file_list = os.listdir(cur_dir)
if "mycreds.txt" in file_list:
    gauth.LoadCredentialsFile("mycreds.txt")
    gauth.LocalWebserverAuth()
else:
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile("mycreds.txt")

# Creates local webserver and auto
# handles authentication.
# gauth.LocalWebserverAuth()       
drive = GoogleDrive(gauth)
username = drive.GetAbout()['user']['displayName']
email = drive.GetAbout()['user']['emailAddress']
print(f"Connected to '{username}' Google Drive, Email: '{email}'")

# Get parent Folder name
parentFolderName = "TrackingActivities"
getParentFolder = drive.ListFile({'q': f"title = '{parentFolderName}' and trashed=false"}).GetList()
if (len(getParentFolder) == 0):
    newFolder = drive.CreateFile({'title': parentFolderName, "mimeType": "application/vnd.google-apps.folder"})
    newFolder.Upload()
    getParentFolder = drive.ListFile({'q': f"title = '{parentFolderName}' and trashed=false"}).GetList()
# Get the first folder found!!!
parentFolder = getParentFolder[0]

# Create folder for each day
today = date.today()
day = today.strftime(r"%d/%m/%Y")
folderName = day
getTodayFolder = drive.ListFile({'q': f"title = '{folderName}' and trashed=false"}).GetList()
if (len(getTodayFolder) == 0):
    newFolder = drive.CreateFile({'title': folderName, "mimeType": "application/vnd.google-apps.folder", 'parents': [{'id': parentFolder['id']}]})
    newFolder.Upload()
    getTodayFolder = drive.ListFile({'q': f"title = '{folderName}' and trashed=false"}).GetList()
# Get the first folder found!!!
todayFolder = getTodayFolder[0]

# This function will check if that file exist on cloud or not
def uploadConfig(fileName):
    cur_dir = os.getcwd()
    file_dir = os.path.join(cur_dir, fileName)
    #Check if exist:
    parentFile = drive.ListFile({'q': f"title = '{fileName}' and trashed=false and '{parentFolder['id']}' in parents"}).GetList()
    if len(parentFile) > 0:  # File exist
        f = parentFile[0]
        f.SetContentFile(file_dir)
        f.Upload()
    else:
        f = drive.CreateFile({'title': fileName, 'parents': [{'id': parentFolder['id']}]})
        f.SetContentFile(file_dir)
        f.Upload()
    #Check if exist:
    todayFile = drive.ListFile({'q': f"title = '{fileName}' and trashed=false and '{todayFolder['id']}' in parents"}).GetList()
    if len(todayFile) > 0:  # File exist
        f = todayFile[0]
        f.SetContentFile(file_dir)
        f.Upload()
    else:
        f = drive.CreateFile({'title': fileName, 'parents': [{'id': todayFolder['id']}]})
        f.SetContentFile(file_dir)
        f.Upload()

uploadConfig("activate.txt")
uploadConfig("endTime.txt")
uploadConfig("history.txt")
uploadConfig("wrongpass.txt")