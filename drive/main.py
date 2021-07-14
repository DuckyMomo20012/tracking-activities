from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

# For using listdir()
import os
# For moving files
import shutil


# Below code does the authentication
# part of the code
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

# replace the value of this variable
# with the absolute path of the directory
# path = r"C:\\Users\\VINH\\Desktop\\drive\\pictures"
   
def upload():
    folderName = str(input("Enter folder's name to upload to: "))
    getFolder = drive.ListFile({'q': f"title = '{folderName}' and trashed=false"}).GetList()
    if (len(getFolder) > 0):
        # Get the first folder found!!!
        folder = getFolder[0]
        cur_upload_des = os.path.join(cur_dir, 'Upload')
        # iterating thought all the files/folder
        # of the desired directory
        for x in os.listdir(cur_upload_des):
        
            f = drive.CreateFile({'title': x, 'parents':[{'id': folder['id']}]})
            f.SetContentFile(os.path.join(cur_upload_des, x))
            f.Upload()
        
            # Due to a known bug in pydrive if we 
            # don't empty the variable used to
            # upload the files to Google Drive the
            # file stays open in memory and causes a
            # memory leak, therefore preventing its 
            # deletion
            f = None
        print("Uploaded")
    else:
        print(f"Folder '{folderName}' not found.")
        
def download():
    fileName = str(input("Enter download file's name: "))
    getFile = drive.ListFile({'q': f"title contains '{fileName}' and trashed=false"}).GetList()
    if len(getFile) > 0:
        # Get the first file found!!!
        print(getFile[0]['title'])
        fileDownloadedName = getFile[0]['title']
        file_id = getFile[0]['id']
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(fileDownloadedName)
        #if mimeType is 'text/plain', 'text/x-python', 'application/json'
        availableTypeToPrintContent = ['text/plain', 'text/x-python', 'application/json']
        if (getFile[0]['mimeType'] in availableTypeToPrintContent):
            print(f"File: '{fileDownloadedName}' Contain: '{file.GetContentString()}'\n")
        print("Downloaded")

        #Get current directory
        cur_dir = os.getcwd()
        #Get file directory
        fileDir = os.path.join(cur_dir, fileDownloadedName)
        target = os.path.join(cur_dir, "Downloads")

        #Move files to "Downloads" folder
        try:
            shutil.move(fileDir, target)
            print(f"{fileDownloadedName} moved to 'Downloads' folder")
        except:
            ans = str(input((f"File {fileDownloadedName} already exist. Do you want to replace it?: (Y/N) ")))
            if "Y" == ans:
                os.replace(fileDir, target)
                print(f"{fileDownloadedName} moved to 'Downloads' folder")
            else:
                print("Canceled")
    else:
        print(f"File '{fileName}' doesn't exist")

def createFolder():
    folderName = str(input("Enter new folder's name: "))
    file_list = drive.ListFile({'q': f"title = '{folderName}' and trashed=false"}).GetList()
    if len(file_list) > 0:
        print(f"Folder '{folderName}' is already exist.")
    else:
        folder = drive.CreateFile({'title': folderName, "mimeType": "application/vnd.google-apps.folder"})
        folder.Upload()
        if (folderName != ""):
            print(f"'{folderName}' created")
        else:
            print("'New Folder' created")

def listFiles():
    file_list = drive.ListFile({'q': 'trashed=false'}).GetList()

    for file in file_list:
        print(file['title'], file['id'])

def removeCred():
    try:
        os.remove("mycreds.txt")
        print("Logout")
    except:
        print("There was an error")

ans = True
while ans:
    print("""
    1.List all files
    2.Create folder
    3.Upload all files from 'Upload' folder
    4.Download file to current directory
    5.Logout
    6.Exit
    """)
    ans = str(input("What would you like to do?: "))
    if "1" == ans:
        listFiles()
    elif "2" == ans:
        print("\nCreate folder:")
        createFolder()
    elif "3" == ans:
        print("\nUpload files:")
        upload()
    elif "4" == ans:
        print("\nDownload files:")
        download()
    elif "5" == ans:
        logout = str(input("Do you want to logout?: (Y/N) "))
        if logout == "Y":
            removeCred()
            ans = False
            print("\nExiting...")
        else:
            print("Canceled")
    elif "6" == ans:
        ans = False
        print("\nExiting...")
    else:
        print("\n Not Valid Choice. Please try again")
