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
# For encrypting string
from cryptography.fernet import Fernet

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

def getSensitiveData(fileName):
    drive = auth()
    # Get the first folder found!!!
    parentFolder = getParentFolder(drive)

    # Lay file o trong folder "TrackingActivities"
    parentFile = drive.ListFile({'q': f"title contains '{fileName}' and trashed=false and '{parentFolder['id']}' in parents"}).GetList()
    if len(parentFile) > 0:
        # Get the first file found!!!
        fileDownloadedName = parentFile[0]['title']
        file_id = parentFile[0]['id']
        file = drive.CreateFile({'id': file_id})
        # Don't download this file
        key = file.GetContentString(fileDownloadedName)
        return key
    else:
        return None
    
def getKey():
    key = getSensitiveData("key.txt")
    if key == None:
        createConfig("key.txt")
        key = Fernet.generate_key() # byte
        keyFile = open("key.txt", "w+")
        keyFile.writelines(key.decode())
        keyFile.close()
        uploadConfig("key.txt")
        os.remove("key.txt")
    if type(key) is str:
        key = key.encode()
    return key

def getPass():
    encrypted_pass = getSensitiveData("password.txt")
    # Key is very important
    if encrypted_pass == None:
        key = getKey()
        print("""
    Please create new password
        """)
        createConfig("password.txt")
        editConfig("password.txt", upload=False)
        # Open to read unencrypted password
        passwordFile = open("password.txt", "r")
        unencrypted_pass = passwordFile.readline()
        passwordFile.close()
        # Encrypt password
        encrypted_pass = encrypt(unencrypted_pass.encode(), key)
        # Open to write encrypted password
        passwordFile = open("password.txt", "w+")
        passwordFile.writelines(encrypted_pass.decode())
        passwordFile.close()
        # Upload to Google Drive
        uploadConfig("password.txt")
        # Remove from local
        os.remove("password.txt")

    if type(encrypted_pass) is str:
        encrypted_pass = encrypted_pass.encode()
    return encrypted_pass

def login():
    print("""
    Loading...
    """)
    key = getKey()
    encrypted_password = getPass()
    decrypted_password = decrypt(encrypted_password, key).decode()
    check = False
    while check == False:
        input_password = str(input("Please enter password: "))
        if input_password == decrypted_password:
            print("""
    Login successfully.
            """)
            check = True
        else:
            print("""
    ERROR: Wrong password. Forgot password?
    NOTE: You can reset password by deleting "password.txt" on Google Drive.
            """)

def auth():
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
    print("Getting Google Drive data. Please wait...")    
    drive = GoogleDrive(gauth)
    return drive

def showInfo():
    drive = auth()
    username = drive.GetAbout()['user']['displayName']
    email = drive.GetAbout()['user']['emailAddress']
    return username, email

### Unused functions 
def upload():
    drive = auth()
    cur_dir = os.getcwd()
    # Upload from Upload folder
    folderName = str(input("Enter folder's name to upload to: "))
    getFolder = drive.ListFile({'q': f"title = '{folderName}' and trashed=false"}).GetList()
    if (len(getFolder) > 0):
        # Get the first folder found!!!
        folder = getFolder[0]
        cur_upload_des = os.path.join(cur_dir, 'Upload')
        if not os.path.exists(cur_upload_des):
            os.makedirs(cur_upload_des)
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

def uploadImage():
    drive = auth()
    cur_dir = os.getcwd()
    # Get the first folder found!!!
    todayFolder = getTodayFolder()

    cur_upload_des = os.path.join(cur_dir, 'Upload')
    if not os.path.exists(cur_upload_des):
        os.makedirs(cur_upload_des)
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

def download():
    drive = auth()
    fileName = str(input("Enter download file's name: "))
    getFile = drive.ListFile({'q': f"title contains '{fileName}' and trashed=false"}).GetList()
    if len(getFile) > 0:
        # Get the first file found!!!
        print(getFile[0]['title'])
        fileDownloadedName = getFile[0]['title']
        file_id = getFile[0]['id']
        fileInfo = drive.CreateFile({'id': file_id})
        fileInfo.GetContentFile(fileDownloadedName)
        #if mimeType is 'text/plain', 'text/x-python', 'application/json'
        availableTypeToPrintContent = ['text/plain', 'text/x-python', 'application/json']
        if (getFile[0]['mimeType'] in availableTypeToPrintContent):
            print(f"File: '{fileDownloadedName}' Contain: '{fileInfo.GetContentString()}'\n")
        print("Downloaded")

        #Get current directory
        cur_dir = os.getcwd()
        #Get file directory
        file_dir = os.path.join(cur_dir, fileDownloadedName)
        target = os.path.join(cur_dir, "Downloads")
        if not os.path.exists(target):
            os.makedirs(target)

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
    drive = auth()
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
            print("'New Folder' created on Google Drive")

def listFiles():
    drive = auth()
    file_list = drive.ListFile({'q': 'trashed=false'}).GetList()

    for files in file_list:
        print(files['title'], files['id'])
###
def removeCred():
    try:
        os.remove("mycreds.txt")
        print("Logout.")
    except:
        print("There was an error.")

def getParentFolder(drive = None):
    if drive == None:
        drive = auth()
    # Get parent Folder name
    parentFolderName = "TrackingActivities"
    getParentFolder = drive.ListFile({'q': f"title = '{parentFolderName}' and trashed=false"}).GetList()
    if (len(getParentFolder) == 0):
        newFolder = drive.CreateFile({'title': parentFolderName, "mimeType": "application/vnd.google-apps.folder"})
        newFolder.Upload()
        getParentFolder = drive.ListFile({'q': f"title = '{parentFolderName}' and trashed=false"}).GetList()
    # Get the first folder found!!!
    return getParentFolder[0]

def getTodayFolder(drive = None):
    if drive == None:
        drive = auth()
    parentFolder = getParentFolder(drive)

    # Create folder for each day
    today = date.today()
    day = today.strftime(r"%d/%m/%Y")
    folderName = day
    getTodayFolder = drive.ListFile({'q': f"title = '{folderName}' and trashed=false"}).GetList()
    if (len(getTodayFolder) == 0):
        newFolder = drive.CreateFile({'title': folderName, "mimeType": "application/vnd.google-apps.folder", 'parents': [{'id': parentFolder['id']}]})
        newFolder.Upload()
        getTodayFolder = drive.ListFile({'q': f"title = '{folderName}' and trashed=false"}).GetList()
    
    # Return the first folder found!!!
    return getTodayFolder[0]

def getParentFolderAndTodayFolder(drive = None):
    if drive == None:
        drive = auth()
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
    
    # Return the first folder found!!!
    return getParentFolder[0], getTodayFolder[0]

def createConfig(fileName):
    cur_dir = os.getcwd()
    file_dir = os.path.join(cur_dir, fileName)
    #Check if exist (LOCAL)
    if not os.path.exists(file_dir):
        # Tao mot file moi khong co noi dung
        newFile = open(fileName, "w+")
        newFile.close()
        print(f"Created {fileName} on local.")
        return True
    return False

def uploadConfig(fileName):
    drive = auth()
    # Upload to both parent folder and today folder!!!

    # Get the first folder found!!!
    parentFolder, todayFolder = getParentFolderAndTodayFolder(drive)

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

def downloadConfig(fileName):
    drive = auth()
    # Get the first folder found!!!
    parentFolder = getParentFolder(drive)

    #Check if file already exits, if it does then remove and download new file
    cur_dir = os.getcwd()
    file_dir = os.path.join(cur_dir, fileName)
    if os.path.exists(file_dir):
        os.remove(file_dir)
    # Lay file o trong folder "TrackingActivities"
    parentFile = drive.ListFile({'q': f"title contains '{fileName}' and trashed=false and '{parentFolder['id']}' in parents"}).GetList()
    if len(parentFile) > 0:
        # Get the first file found!!!
        print(f"Downloaded {parentFile[0]['title']}.")
        fileDownloadedName = parentFile[0]['title']
        file_id = parentFile[0]['id']
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(fileDownloadedName)
    else:
        print(f"ERROR: File '{fileName}' doesn't exist.")

def checkEmpty(fileName):
    readFile = open(f"{fileName}", "r")
    data = readFile.readlines()
    if len(data) == 0:
        print(f"""
    ERROR: File {fileName} can't be empty.
    NOTE: You should go to "README.txt" to see examples. 
        """)
        readFile.close()
        return False
    readFile.close()
    return True
   
def checkFormat(fileName):
    readFile = open(f"{fileName}", "r")
    reg = r"^F[0-2]\d:[0-5]\d\sT[0-2]\d:[0-5]\d(|\sD\d+\sI\d+\sS\d+|\sS\d+)$"
    data = readFile.readlines()
    for index, lines in enumerate(data):
        find = re.search(reg, lines)
        if find is None:
            print(f"""
            ERROR: There was an error in line {index + 1} in '{fileName}'. 
            Please edit line {index + 1} to correct format below:
            F<h1:m1> T<h2:m2>|D<mD> I<mI>|S<mS>
             NOTE: remember to remove redundant space at the end of line
            """)
            readFile.close()
            return False
    readFile.close()
    return True

def sortLines(fileName):
    readFile = open(f"{fileName}", "r")
    data = readFile.readlines()
    readFile.close()
    for time in data:
        h, m = time.split(" ")[0][1:].split(":")
        toTime = h * 60 + m # We will use toTime to sort in code below
    # time.split(" ")[0][1:].split(":")[0] tuong tu nhu h
    # time.split(" ")[0][1:].split(":")[1]) tuong tu nhu m
    data.sort(key=lambda time: time.split(" ")[0][1:].split(":")[0] * 60 + time.split(" ")[0][1:].split(":")[1])
    
    newData = data.copy()

    writeFile = open(f"{fileName}", "w+")
    for lines in newData:
        writeFile.writelines(lines)
    writeFile.close()
    print(f"File {fileName} sorted.")

def removeDuplicateAndBlankLines(fileName):
    readFile = open(f"{fileName}", "r")
    data = readFile.readlines()
    readFile.close()

    data = list(dict.fromkeys(data))

    # Boi vi line cuoi khong co "\n" nen co the duplicate.
    # Them vao do file da dc sort o ham sortLines() nen chi check 
    # 2 dong cuoi cung va dong cuoi thu 2, dong cuoi thu 2
    # se bo di "\n" de so sanh vs dong cuoi.
    # Dong thoi phai dam bao tat ca so dong > 1
    if len(data) > 1 and data[-1] == data[-2].strip("\n"):
        data.remove(data[-1])

    if "\n" in data:
        data.remove("\n")

    newData = data.copy()

    writeFile = open(f"{fileName}", "w+")
    for lines in newData:
        writeFile.writelines(lines)
    writeFile.close()
    print(f"File {fileName} removed duplicates and blank lines.")

def stripLastLineEndLine(fileName):
    readFile = open(f"{fileName}", "r")
    data = readFile.readlines()
    readFile.close()

    #Won't check if file is empty
    if len(data) > 0:
        data[-1] = data[-1].strip("\n")

    newData = data.copy()

    writeFile = open(f"{fileName}", "w+")
    for lines in newData:
        writeFile.writelines(lines)
    writeFile.close()
    print(f"File {fileName} stripped last line's endline.")    

def fixLines(fileName, lineToFix, newLine):
    readFile = open(f"{fileName}", "r")
    data = readFile.readlines()
    readFile.close()
    newData = data.copy()
    # Assign old lines to new line
    newData[lineToFix] = newLine
    writeFile = open(f"{fileName}", "w+")
    for lines in newData:
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

        # Boi vi check format o tren tim ra nhung dong khong hop le 
        # la co dau "-" nen o day cac co khong the la so am nen khong can check lai nua

        fromTime = F[1:].split(":")
        fromTimeToMin = int(fromTime[0]) * 60 + int(fromTime[1])
        toTime = T[1:].split(":")
        toTimeToMin = int(toTime[0]) * 60 + int(toTime[1])
        availableTime = toTimeToMin - fromTimeToMin
        if availableTime <= 0:
            print(f"""
    ERROR: Wrong 'from' and 'to' time in line {index + 1}. 
    'T' time should be bigger than 'F' time.
            """)
            readFile.close()
            return False
        sumTime = 0
        if S != "":
            sumTime = int(S[1:])
            # S co the bang voi availableTime
            if (sumTime > availableTime):
                print(f"""
    ERROR: Wrong 'sum' time in line {index + 1}. 
    'S' time should be smaller than available time.
                """)
                readFile.close()
                return False
            if (sumTime == 0):
                print(f"""
    ERROR: Wrong 'sum' time in line {index + 1}. 
    'S' can't be Zero.
                """)
                readFile.close()
                return False
        durationTime = 0
        if D != "":
            durationTime = int(D[1:])
            # D co the bang voi S, se duoc optimize tu dong
            if durationTime > sumTime:
                print(f"""
    ERROR: Wrong 'duration' time in line {index + 1}. 
    'D' time should be smaller than sum time.
                """)
                readFile.close()
                return False
            if durationTime == 0:
                print(f"""
    ERROR: Wrong 'duration' time in line {index + 1}. 
    'D' can't be Zero.
                """)
                readFile.close()
                return False
                
        interruptTime = 0
        if I != "":
            # Neu chi so sanh lon hon thi luc do I + D = S nhung D = 0 thi se tra ve ERROR
            interruptTime = int(I[1:])
            if (interruptTime >= sumTime):
                print(f"""
    ERROR: Wrong 'interrupt' time in line {index + 1}. 
    'I' time should be smaller than sum time.
                """)
                readFile.close()
                return False
        # D + I co the bang voi S
        if durationTime + interruptTime > sumTime:
            print(f"""
    ERROR: Wrong 'duration' and 'interrupt' time in line {index + 1}. 
    'D' + 'I' time should be smaller than 'S' time.
            """)
            readFile.close()
            return False

        if (D == "" and I == "" and sumTime == availableTime):
            newLines = f"{F} {T}\n"
            fixLines(fileName, index, newLines)
            oldText = data[index].strip("\n")
            newText = newLines.strip("\n")
            print(f"""
    Line[{index + 1}] optimized 
    From '{oldText}' 
    To '{newText}'
            """)
        if D != "" and I != "" and durationTime == sumTime and interruptTime == 0:
            # S da co san "\n" nen khong can them nua 😡😡😡
            newLines = f"{F} {T} {S}"
            fixLines(fileName, index, newLines)
            oldText = data[index].strip("\n")
            newText = newLines.strip("\n")
            print(f"""
    Line[{index + 1}] optimized 
    From '{oldText}' 
    To '{newText}'
            """)

    readFile.close()
    return True

def checkConflict(fileName):
    readFile = open(f"{fileName}", "r")
    data = readFile.readlines()
    if len(data) > 1:
        for index, lines in enumerate(data):
            # skip first element
            if index == 0:
                continue
            currentInfo = lines.split(" ")
            # currentInfo[0] to get from time
            currentFromTime = currentInfo[0][1:].split(":") # Remove "F" from info and split by ":"
            currentFromTimeToMin = int(currentFromTime[0]) * 60 + int(currentFromTime[1])
            previousInfo = data[index - 1].split(" ")
            # previousInfo[1] to get to time
            previousToTime = previousInfo[1][1:].split(":") # Remove "T" from info and split by ":"
            previousToTimeToMin = int(previousToTime[0]) * 60 + int(previousToTime[1])
            if previousToTimeToMin >= currentFromTimeToMin:
                print(f"""
    Conflict between line {index - 1 + 1} and line {index + 1}.
    Please fix it and try again.
                """)
                readFile.close()
                return False
    readFile.close()
    return True

def checkFileOpening(processName, fileName):
    #Note: processName = "notepad.exe"
    while (True):
        opening = False
        for proc in psutil.process_iter():
            #Check if any notepad.exe is opening 
            if (proc.name() == processName):
                # Check reg boi vi co the la C:\\fileName\test.txt, khong 
                # phai la file minh mong muon
                reg = r"[^\\]*\.txt"
                #cmd format: ['C:\\Windows\\system32\\NOTEPAD.EXE', 'C:\\Users\\VINH\\Desktop\\solution', 'source.txt']
                cmd = proc.cmdline()
                # If file name contains "space" character, then we have to join 
                # all strings
                pathFileOpening = "".join(cmd[1:])
                # Strip previous path
                # Ex: C:\Users\VINH\Desktop\TEST.txt, keeps only TEST.txt
                fileOpening = re.search(reg, pathFileOpening)
                if (fileOpening.group() == fileName):
                    opening = True
                    time.sleep(1) # Delay 1 second
                    break
        if opening == False:
            break

    print(f"File {fileName} closed.")

def editConfig(fileName, upload = True):
    if platform.system() == "Windows":
        check = False
        while(check == False):
            os.startfile(fileName)
            print(f"'{fileName}' opened in Notepad")
            print(f"Please close '{fileName}' to continue")

            checkFileOpening("notepad.exe", fileName)

            removeDuplicateAndBlankLines(fileName)
            stripLastLineEndLine(fileName)
            # Normal file doesn't require checking 
            check = True
            if fileName == "activate.txt":
                # Check format first
                if checkFormat(fileName) == True:
                    sortLines(fileName)
                    removeDuplicateAndBlankLines(fileName)
                    stripLastLineEndLine(fileName)
                    # Check conflicts then check logic
                    check = checkConflict(fileName) and checkLogic(fileName)
                else:
                    check = False

        if upload == True:
            uploadConfig(fileName)
            print(f"Uploaded {fileName} to Google Drive.")
            # De user khong the edit thi co the remove file sau khi edit xong
            os.remove(fileName)

def downloadImage(folderName):
    drive = auth()
    parentFolderName = folderName
    # Khong dung getParentFolder() boi vi cai nay la de quy !!!
    getParentFolder = drive.ListFile({'q': f"title = '{parentFolderName}' and trashed=false"}).GetList()
    if (len(getParentFolder) == 0):
        newFolder = drive.CreateFile({'title': parentFolderName, "mimeType": "application/vnd.google-apps.folder"})
        newFolder.Upload()
        getParentFolder = drive.ListFile({'q': f"title = '{parentFolderName}' and trashed=false"}).GetList()
    # Get the first folder found!!!
    # Get the first folder found!!!
    parentFolder = getParentFolder[0]
    getFile = drive.ListFile({'q': f"trashed=false and '{parentFolder['id']}' in parents"}).GetList()

    cur_dir = os.getcwd()
    # Because todayFolder format is "dd/mm/YYYY" so we have to replace "/" with "_"
    newParentFolderName = parentFolderName.replace(r"/", "_")
    target = os.path.join(cur_dir, f"Downloads\\{newParentFolderName}")
    
    if not os.path.exists(target):
        os.makedirs(target)

    for files in getFile:
        # Get the first file found!!!
        # normal file mimeType is 'text/plain'. If mimeType is 'application/vnd.google-apps.folder'
        # then we have to recursively go to that folder and download files within it
        if (files['mimeType'] == 'application/vnd.google-apps.folder'):
            downloadImage(files['title'])
        else:
            fileDownloadedName = files['title']
            file_id = files['id']
            fileInfo = drive.CreateFile({'id': file_id})

            # if this file didn't exist then download
            if not os.path.exists(os.path.join(target, fileDownloadedName)):
                file_dir = os.path.join(cur_dir, fileDownloadedName)
                fileInfo.GetContentFile(fileDownloadedName)
                # Boi vi ten thu muc da ton tai nen se khong in ra ten thu muc download
                print(f"Downloaded {files['title']} from {newParentFolderName} folder.")
                shutil.move(file_dir, target)
            else:
                print(f"File {files['title']} from {newParentFolderName} folder already exist.")

def removeFolder(path):
    shutil.rmtree(path)