import os
import datetime
import ast
import googleapiclient.errors

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from os import chdir, listdir, stat
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList
from glob import glob
from sys import exit

# https://gist.github.com/jmlrt/f524e1a45205a0b9f169eb713a223330
def get_folder_id(drive, parent_folder_id, folder_name):
    """ 
        Check if destination folder exists and return it's ID
    """

    # Auto-iterate through all files in the parent folder.
    file_list = GoogleDriveFileList()
    try:
        file_list = drive.ListFile(
            {'q': "'{0}' in parents and trashed=false".format(parent_folder_id)}
        ).GetList()
    # Exit if the parent folder doesn't exist
    except googleapiclient.errors.HttpError as err:
        # Parse error message
        message = ast.literal_eval(err.content)['error']['message']
        if message == 'File not found: ':
            print(message + folder_name)
            exit(1)
        # Exit with stacktrace in case of other error
        else:
            raise

    # Find the the destination folder in the parent folder's files
    for file1 in file_list:
        if file1['title'] == folder_name:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
            return file1['id']

# https://gist.github.com/jmlrt/f524e1a45205a0b9f169eb713a223330
def create_folder(drive, folder_name, parent_folder_id):
    """ 
    Create folder on Google Drive
    """
    
    folder_metadata = {
        'title': folder_name,
        # Define the file type as folder
        'mimeType': 'application/vnd.google-apps.folder',
        # ID of the parent folder        
        'parents': [{"kind": "drive#fileLink", "id": parent_folder_id}]
    }

    folder = drive.CreateFile(folder_metadata)
    folder.Upload()

    # Return folder informations
    print('title: %s, id: %s' % (folder['title'], folder['id']))
    return folder['id']

# https://gist.github.com/jmlrt/f524e1a45205a0b9f169eb713a223330
def upload_files(drive, folder_id, src_folder_name):
    """ 
        Upload files in the local folder to Google Drive 
    """

    # Enter the source folder
    try:
        chdir(src_folder_name)
    # Print error if source folder doesn't exist
    except OSError:
        print(src_folder_name + 'is missing')
    # Auto-iterate through all files in the folder.
    for file1 in listdir('.'):
        # Check the file's size
        print(src_folder_name)
        statinfo = stat(file1)
        if statinfo.st_size > 0:
            print('uploading ' + file1)
            # Upload file to folder.
            f = drive.CreateFile(
                {"parents": [{"kind": "drive#fileLink", "id": folder_id}]})
            f.SetContentFile(file1)
            f.Upload()
        # Skip the file if it's empty
        else:
            print('file {0} is empty'.format(file1))


def main():
    os.chdir('/Users/liam_msg/Documents/automate_MSG_automate_recharge')

    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds")

    drive = GoogleDrive(gauth)

    lastday= datetime.date.today().replace(day=1)
    firstday = lastday - datetime.timedelta(days=1)
    firstday =firstday.replace(day=1)

    recharge_fp = glob(os.path.join('monthlyRechargesTemp',
        '{fyyyy}-{fmm:02}-01_TO_{yyyy}-{mm:02}-01'.format(
            fyyyy=firstday.year,
            fmm=firstday.month,
            yyyy=lastday.year,
            mm=lastday.month),"*.xlsx"))

    try:
        file_name = recharge_fp[0].split('/')[-1]
    except IndexError:
        print("Was unable to upload rechargeSummary for this month. Time to fix bugs!")
        exit(1)
    folder_id ='1o14IjFlRZW4HN0ULdhdYvtpgqvMcx9GU'
    file1 = drive.CreateFile(
        {'title':file_name,
        "parents": [{"kind": "drive#fileLink","id": folder_id}]})
    file1.SetContentFile(recharge_fp[0])
    file1.Upload()
    print("success!")

if __name__ == '__main__':
    main()
