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
cur_upload_des = os.path.join(cur_dir, 'Upload')
# iterating thought all the files/folder
# of the desired directory
for x in os.listdir(cur_upload_des):

    f = drive.CreateFile({'title': x, 'parents':[{'id': todayFolder['id']}]})
    f.SetContentFile(os.path.join(cur_upload_des, x))
    f.Upload()
    # Due to a known bug in pydrive if we 
    # don't empty the variable used to
    # upload the files to Google Drive the
    # file stays open in memory and causes a
    # memory leak, therefore preventing its 
    # deletion
    f = None
for x in os.listdir(cur_upload_des):
    os.remove(os.path.join(cur_upload_des, x))