from datetime import datetime, date, timedelta
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


def main():
    os.chdir('.')
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

    today = datetime.date.today()
    first = today.replace(day=1)
    current_month = first.month
    current_year = first.year

    last_month_date = first - datetime.timedelta(days=1)
    last_month = last_month_date.month

    last_year = last_month_date.year

    cold_log = "4c_{pmonth}_01_{pyear}_TO_{month}_01_{year}.txt".format(
        month=current_month, year=str(current_year),
        pmonth=last_month, pyear=str(last_year))
    room_log = "20c_{pmonth}_1_{pyear}_TO_{month}_1_{year}.txt".format(
        month=current_month, year=str(current_year),
        pmonth=last_month, pyear=str(last_year))

    room_folder_id = '1Bk8D2ZkbpX3kkJHLM1lduPTD_RbCiXDN'
    cold_folder_id = '1U1a6RnhTr37n3BUFEmA4K4j7D6titeMv'

    # print(cold_log)
    # room_file_list = drive.ListFile({'q': "'1Bk8D2ZkbpX3kkJHLM1lduPTD_RbCiXDN' in parents and trashed=false"}).GetList()
    gdrive_room_list = drive.ListFile(
        {'q': "'1Bk8D2ZkbpX3kkJHLM1lduPTD_RbCiXDN' in parents and trashed=false"}).GetList()
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
        {'q': "'1U1a6RnhTr37n3BUFEmA4K4j7D6titeMv' in parents and trashed=false"}).GetList()
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
