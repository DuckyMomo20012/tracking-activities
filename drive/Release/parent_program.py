from lib import *

drive = auth()
username, email = showInfo()
        
ans = True
while ans:
    print(f"'{username}' Google Drive, Email: '{email}'")
    print("""

    1.View history.
    2.Edit 'activate.txt'.
    3.Delete 'Downloads' folder.
    4.Logout.
    5.Exit.
    """)
    ans = str(input("What would you like to do?: "))
    if "1" == ans:
        downloadImage("TrackingActivities")
        os.startfile(f"{os.getcwd()}\Downloads")
    elif "2" == ans:
        downloadConfig("activate.txt")
        createConfig("activate.txt")
        editConfig("activate.txt")
    elif "3" == ans:
        logout = str(input("Do you want to delete 'Download' folder?: (Y/N) "))
        if logout == "Y":
            ### DON'T CHANGE THIS!!!!!
            ### IT WILL REMOVE ALL THE FILES YOU HAVE IF YOU CHANGE DIRECTORY!!!!
            removeImage(f"{os.getcwd()}\\Downloads")
            ###
        else:
            print("Canceled")
    elif "4" == ans:
        logout = str(input("Do you want to logout?: (Y/N) "))
        if logout == "Y":
            removeCred()
            ans = False
            print("\nExiting...")
        else:
            print("Canceled.")
    elif "5" == ans:
        ans = False
        print("\nExiting...")
    else:
        print("\n Not Valid Choice. Please try again.")