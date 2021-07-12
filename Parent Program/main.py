from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

# For using listdir()
import os
# For moving files
import shutil
# For checking platform's name
import platform
# For RegEx check
import re
# For process manipulation
import psutil
# For get current today
from datetime import date
# Sleep
import time
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
username = drive.GetAbout()['user']['displayName']
email = drive.GetAbout()['user']['emailAddress']
print(f"Connected to '{username}' Google Drive, Email: '{email}'")

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
        file_dir = os.path.join(cur_dir, fileDownloadedName)
        target = os.path.join(cur_dir, "Downloads")

        #Move files to "Downloads" folder
        if os.path.exists(file_dir):
            ans = str(input((f"File {fileDownloadedName} already exist. Do you want to replace it?: (Y/N) ")))
            if "Y" == ans:
                os.remove(file_dir)
                shutil.move(file_dir, target)
                print(f"{fileDownloadedName} moved to 'Downloads' folder")
            else:
                print("Canceled")
        else:
            shutil.move(file_dir, target)
            print(f"{fileDownloadedName} moved to 'Downloads' folder")
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

def checkFormat(fileName):
    readFile = open(f"{fileName}", "r")
    reg = r"^F[0-2]\d:[0-5]\d\sT[0-2]\d:[0-5]\d(|\sD\d+\sI\d+\sS\d+|\sS\d+)$"
    data = readFile.readlines()
    for lines in data:
        find = re.search(reg, lines)
        if find is None:
            print(f"""
            There was an error in '{fileName}'. 
            Please edit '{fileName}' to correct format below:
            F<h1:m1> T<h2:m2>|D<mD> I<mI>|S<mS>
            """)
            return False
    readFile.close()
    return True

def fixLines(fileName, lineToFix, newData):
    readFile = open(f"{fileName}", "r")
    data = readFile.readlines()
    readFile.close()
    data[lineToFix] = newData
    writeFile = open(f"{fileName}", "w+")
    for lines in data:
        writeFile.writelines(lines)
    writeFile.close()

def checkLogic(fileName):
    readFile = open(f"{fileName}", "r")
    data = readFile.readlines()
    for index, lines in enumerate(data):
        F, T, D, I, S = ["", "", "", "", ""]
        pack = lines.split(" ")
        if 2 == len(pack):
            F, T  = pack
        elif 3 == len(pack):
            F, T, S = pack
        else:
            F, T, D, I, S = pack

        fromTime = F[1:].split(":")
        fromTimeToMin = int(fromTime[0]) * 60 + int(fromTime[1])
        toTime = T[1:].split(":")
        toTimeToMin = int(toTime[0]) * 60 + int(toTime[1])
        availableTime = toTimeToMin - fromTimeToMin
        if availableTime <= 0:
            print("""
            ERROR: Wrong 'from' and 'to' time. 
            'T' time should be bigger than 'F' time
            """)
            return False
        sumTime = 0
        if S != "":
            sumTime = int(S[1:])
            if (sumTime > availableTime):
                print("""
                ERROR: Wrong 'sum' time. 
                'S' time should be smaller than available time
                """)
                return False
        durationTime = 0
        if D != "":
            durationTime = int(D[1:])
            if durationTime > availableTime: # range from 0 <= durationTime <= availableTime
                print("""
                ERROR: Wrong 'duration' time. 
                'D' time should be smaller than available time
                """)
                return False
            if durationTime == 0:
                pass
                
        interruptTime = 0
        if I != "":
            # availableInterruptTime = 
            interruptTime = int(I[1:])
            if (interruptTime > availableTime): # range from 0 <= interruptTime <= availableTime
                print("""
                ERROR: Wrong 'interrupt' time. 
                'I' time should be smaller than available time
                """)
                return False

        if durationTime + interruptTime > availableTime:
            print("""
            ERROR: Wrong 'duration' and 'interrupt' time. 
            'D' + 'I' time should be smaller than 'S' time
            """)
            return False

        if (sumTime == availableTime and durationTime == 0 and interruptTime == 0):
            newLines = f"{F} {T}"
            print(f"""
            Line[{index}] optimized 
            From '{data[index]}' 
            To '{newLines}'
            """)
            fixLines(fileName, index, newLines)
        if durationTime == sumTime and interruptTime == 0:
            newLines = f"{F} {T} {S}"
            print(f"""
            Line[{index}] optimized 
            From '{data[index]}' 
            To '{newLines}'
            """)
            fixLines(fileName, index, newLines)

    readFile.close()
    return True

def sortLines(fileName):
    readFile = open(f"{fileName}", "r")
    data = readFile.readlines()
    readFile.close()
    for time in data:
        h, m = time.split(" ")[0][1:].split(":")
        toTime = h * 60 + m # We will use toTime to sort in code below

    data.sort(key=lambda time: time.split(" ")[0][1:].split(":")[0] * 60 + time.split(" ")[0][1:].split(":")[1])
    
    newData = data

    writeFile = open(f"{fileName}", "w+")
    for lines in newData:
        writeFile.writelines(lines)
    writeFile.close()
    print(f"""
    File {fileName} sorted
    """)

def uploadConfig(fileName):
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

    cur_dir = os.getcwd()
    file_dir = os.path.join(cur_dir, fileName)
    #Check if exist:
    getFile = drive.ListFile({'q': f"title = '{fileName}' and trashed=false and '{todayFolder['id']}' in parents"}).GetList()
    if len(getFile) > 0:  # File exist
        f = getFile[0]
        f.SetContentFile(file_dir)
        f.Upload()
    else:
        f = drive.CreateFile({'title': fileName, 'parents': [{'id': todayFolder['id']}]})
        f.SetContentFile(file_dir)
        f.Upload()

def downloadConfig(fileName):
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

    #Check if file already exits, if it does then remove and download new file
    cur_dir = os.getcwd()
    file_dir = os.path.join(cur_dir, fileName)
    if os.path.exists(file_dir):
        os.remove(file_dir)
    # Lay file o trong folder "TrackingActivities"
    getFile = drive.ListFile({'q': f"title contains '{fileName}' and trashed=false and '{todayFolder['id']}' in parents"}).GetList()
    if len(getFile) > 0:
        # Get the first file found!!!
        print(getFile[0]['title'])
        fileDownloadedName = getFile[0]['title']
        file_id = getFile[0]['id']
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(fileDownloadedName)
    else:
        print(f"File '{fileName}' doesn't exist")

def editConfig(fileName):
    if platform.system() == "Windows":
        check = False
        while(check == False):
            os.startfile(fileName)
            print("activate.txt opened in Notepad")
            print(f"Please close '{fileName} to continue")
            while (True):
                found = False
                for proc in psutil.process_iter():
                    #Check if any notepad.exe is opening 
                    if (proc.name() == "notepad.exe"):
                        # Check reg boi vi co the la C:\\fileName\test.txt, khong 
                        # phai la file minh mong muon
                        reg = r"[^\\]*\.txt"
                        #cmd format: ['C:\\Windows\\system32\\NOTEPAD.EXE', 'C:\\Users\\VINH\\Desktop\\solution', 'source.txt']
                        cmd = proc.cmdline()
                        # If file name contains "space", then we have to join 
                        # all strings
                        pathFileOpening = "".join(cmd[1:])
                        # Strip previous path
                        # Ex: C:\Users\VINH\Desktop\TEST.txt, keeps only TEST.txt
                        fileOpening = re.search(reg, pathFileOpening)
                        if (fileOpening.group() == fileName):
                            found = True
                            time.sleep(1)
                if (found == False):
                    break
            
            sortLines(fileName)
            check = checkFormat(fileName) and checkLogic(fileName)

        uploadConfig(fileName)

def uploadImage():
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

def downloadImage(folderName):
    parentFolderName = folderName
    getParentFolder = drive.ListFile({'q': f"title = '{parentFolderName}' and trashed=false"}).GetList()
    # Get the first folder found!!!
    parentFolder = getParentFolder[0]
    getFile = drive.ListFile({'q': f"trashed=false and '{parentFolder['id']}' in parents"}).GetList()

    cur_dir = os.getcwd()
    target = os.path.join(cur_dir, "Downloads")

    for files in getFile:
        # Get the first file found!!!
        print(files['title'])
        # normal file mimeType is 'text/plain'. If mimeType is 'application/vnd.google-apps.folder'
        # then we have to recursively go to that folder and download files within it
        if (files['mimeType'] == 'application/vnd.google-apps.folder'):
            downloadImage(files['title'])
        else:
            fileDownloadedName = files['title']
            file_id = files['id']
            file = drive.CreateFile({'id': file_id})
            file.GetContentFile(fileDownloadedName)

            file_dir = os.path.join(cur_dir, fileDownloadedName)
            shutil.move(file_dir, target)

def removeImage(path):
    for files in os.listdir(path):
        os.remove(os.path.join(path, files))
        
ans = True
while ans:
    print(f"'{username}' Google Drive, Email: '{email}'")
    print("""
    1.View history
    2.Edit 'activate.txt'
    3.Logout
    4.Exit
    """)
    ans = str(input("What would you like to do?: "))
    if "1" == ans:
        downloadImage("TrackingActivities")
        os.startfile(f"{os.getcwd()}\Downloads")
    elif "2" == ans:
        downloadConfig("activate.txt")
        editConfig("activate.txt")
    elif "3" == ans:
        logout = str(input("Do you want to logout?: (Y/N) "))
        if logout == "Y":
            removeCred()
            ans = False
            print("\nExiting...")
        else:
            print("Canceled")
    elif "4" == ans:
        ans = False
        print("\nRemoving files from 'Downloads' folder...")
        ### DON'T CHANGE THIS!!!!!
        removeImage(f"{os.getcwd()}\\Downloads")
        ###
        print("\nExiting...")
    else:
        print("\n Not Valid Choice. Please try again")