import os
import subprocess

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

    subprocess.run("cp ./temp/*.txt ./rockimagerBacklogs/".split(" "))

    print("uploading to google drive")
    uploadGDriveMonthlyRecharges.main()

if __name__ == '__main__':
    main()