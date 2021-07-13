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

# Thu muc cha de lay file "configTime.txt"
parentFolderName = "TrackingActivities"
getParentFolder = drive.ListFile({'q': f"title = '{parentFolderName}' and trashed=false"}).GetList()
if (len(getParentFolder) == 0):
    newFolder = drive.CreateFile({'title': parentFolderName, "mimeType": "application/vnd.google-apps.folder"})
    newFolder.Upload()
    getParentFolder = drive.ListFile({'q': f"title = '{parentFolderName}' and trashed=false"}).GetList()
# Get the first folder found!!!
parentFolder = getParentFolder[0]

# # Create folder for each day
# today = date.today()
# day = today.strftime(r"%d/%m/%Y")
# folderName = day
# getTodayFolder = drive.ListFile({'q': f"title = '{folderName}' and trashed=false"}).GetList()
# if (len(getTodayFolder) == 0):
#     newFolder = drive.CreateFile({'title': folderName, "mimeType": "application/vnd.google-apps.folder", 'parents': [{'id': parentFolder['id']}]})
#     newFolder.Upload()
#     getTodayFolder = drive.ListFile({'q': f"title = '{folderName}' and trashed=false"}).GetList()
# # Get the first folder found!!!
# todayFolder = getTodayFolder[0]

def downloadConfig(fileName):
    #Check if file already exits, if it does then remove and download new file
    cur_dir = os.getcwd()
    file_dir = os.path.join(cur_dir, fileName)
    if os.path.exists(file_dir):
        os.remove(file_dir)
    # Lay file o trong folder "TrackingActivities"
    getFile = drive.ListFile({'q': f"title contains '{fileName}' and trashed=false and '{parentFolder['id']}' in parents"}).GetList()
    if len(getFile) > 0:
        # Get the first file found!!!
        print(getFile[0]['title'])
        fileDownloadedName = getFile[0]['title']
        file_id = getFile[0]['id']
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(fileDownloadedName)
    else:
        print(f"File '{fileName}' doesn't exist")

downloadConfig("activate.txt")
downloadConfig("endTime.txt")
downloadConfig("history.txt")
downloadConfig("wrongpass.txt")