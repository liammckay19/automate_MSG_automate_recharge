import os

import downloadRockimagerFiles
import calculateRecharge_auto
import uploadGDriveMonthlyRecharges

def main():
    if not os.path.exists("./rockimagerBacklogs/"):
        os.mkdir("./rockimagerBacklogs/")
    if not os.path.exists("./temp"):
        os.mkdir("./temp")

    print("Downloading rockimager log files from Google Drive")
    downloadRockimagerFiles.main()

    print("calculating recharge")
    calculateRecharge_auto.main()

    os.system("mv ./temp/*.txt ./rockimagerBacklogs/")

    print("uploading to google drive")
    uploadGDriveMonthlyRecharges.main()

if __name__ == '__main__':
    main()