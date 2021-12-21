from datetime import datetime as dt, date, timedelta
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from glob import glob
import datetime
import subprocess


def file_matches_date(str1, str2, acceptable_wrong):
    matches = 0
    temp_str1 = str1
    temp_str2 = str2

    str1 = str1.replace('0', '')
    str2 = str2.replace('0', '')
    for i, c in enumerate(str1):
        if c in str2[i - 2:i + 2]:
            matches += 1
    if (matches >= len(str1) - 1 - acceptable_wrong):
        print("Found on Google Drive: ", temp_str1, temp_str2, True)
    return (matches >= len(str1) - 1 - acceptable_wrong)


def connect_google_drive_api():
    
    # use Gdrive API to access Google Drive
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive
    gauth = GoogleAuth()
    
    # Try to load saved client credentials
    try:
        gauth.LoadCredentialsFile("mycreds.txt")

    except UnboundLocalError:
        pass
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()

    gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script    
    
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)
    
    return drive


def lookForGL_DPE_ExcelFiles(dates=[]):
    drive = connect_google_drive_api()

    today = datetime.date.today()
    if dates:
        today = dates[0]
    first = today.replace(day=1)
    current_month = first.month
    current_year = first.year
    if dates:
        last_month_date = dates[1]
    last_month_date = first - datetime.timedelta(days=1)
    last_month = last_month_date.month

    last_year = last_month_date.year

    excelOriginals = '1UBSK8Q-LsTDccd2o35xMZWMHy7odCZrB'    
    excelOriginals_list = drive.ListFile(
        {'q': "'"+excelOriginals+"' in parents and trashed=false"}).GetList()
    excelOriginalsFound = set()
    for file in excelOriginals_list:
        date = last_month_date.strftime('%b_%Y')
        if date.lower() in file['title']:
            excelOriginalsFound.add(file['title'])
    if len(excelOriginalsFound) == 2:
        return
    else:
        print("Excel files for GL + DPE not found. searching:"+date.lower()+". Please add to the folder with Google Drive ID: "+excelOriginals)
        exit(1)

def main(dates=[]):

    if os.path.exists("temp/"):
        subprocess.run(['rm','-r','temp'])
        subprocess.run(['mkdir','temp'])


    drive = connect_google_drive_api()

    today = datetime.date.today()
    if dates:
        today = dates[1]
    first = today.replace(day=1)
    current_month = first.month
    current_year = first.year

    last_month_date = first - datetime.timedelta(days=1)
    last_month = last_month_date.month

    last_year = last_month_date.year

    lookForGL_DPE_ExcelFiles(dates)

    cold_log = "4c_{pmonth}_01_{pyear}_TO_{month}_01_{year}.txt".format(
        month=current_month, year=str(current_year),
        pmonth=last_month, pyear=str(last_year))
    room_log = "20c_{pmonth}_1_{pyear}_TO_{month}_1_{year}.txt".format(
        month=current_month, year=str(current_year),
        pmonth=last_month, pyear=str(last_year))

    room_folder_id = '1xlE5MW5Lyetb8IqCqfz62LQNVkE17pSv'
    cold_folder_id = '12o6Hl6rVPmgaB3YJZTSeATjTk9tw9oCC'

    # print(cold_log)
    # room_file_list = drive.ListFile({'q': "'1xlE5MW5Lyetb8IqCqfz62LQNVkE17pSv' in parents and trashed=false"}).GetList()
    gdrive_room_list = drive.ListFile(
        {'q': "'"+room_folder_id+"' in parents and trashed=false"}).GetList()
    for gdrive_room_file in gdrive_room_list:
        if file_matches_date(gdrive_room_file['title'], room_log, 1):
            room_log_id = gdrive_room_file['id']

    try:
        download_room_log = drive.CreateFile({'id': room_log_id})
    except UnboundLocalError:
        print("Could not find match for room log file for", room_log, "\n Is the file in Google Drive?")
        exit(1)
    download_room_log.GetContentFile(filename="temp/" + room_log)

    gdrive_cold_list = drive.ListFile(
        {'q': "'"+cold_folder_id+"' in parents and trashed=false"}).GetList()
    for gdrive_cold_file in gdrive_cold_list:
        if file_matches_date(gdrive_cold_file['title'], cold_log, 1):
            cold_log_id = gdrive_cold_file['id']

    try:
        download_cold_log = drive.CreateFile({'id': cold_log_id})
    except UnboundLocalError:
        print("Could not find match for cold log file for", cold_log, "\n Is the file in Google Drive?")
        exit(1)
    download_cold_log.GetContentFile(filename="temp/" + cold_log)

    cold_local = sorted(glob("temp/4c*"))[0]
    room_local = sorted(glob("temp/20c*"))[0]
    subprocess.run(["cp", cold_local, "./rockimagerBacklogs/"])
    subprocess.run(["cp", room_local, "./rockimagerBacklogs/"])


if __name__ == '__main__':
    main()
