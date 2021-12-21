import os
from datetime import datetime, date, timedelta
import subprocess

import downloadRockimagerFiles
import calculateRecharge_auto
import uploadGDriveMonthlyRecharges
import googleDriveUtils as gdrive


def askForDates():
    start_date, end_date = "", ""
    while 1:
        try:
            start_date = datetime.strptime(
                input("Enter Start date in the format yyyy-m-d: "), "%Y-%m-%d"
            )
            end_date = datetime.strptime(
                input("Enter End date in the format yyyy-m-d: ") + "-23-59-59",
                "%Y-%m-%d-%H-%M-%S",
            )
            if start_date > end_date:
                raise ValueError
            break
        except ValueError as e:
            print(
                "\nInvalid date range or wrong format. Please try again or ctrl+C and ENTER to exit."
            )

    dates = [start_date, end_date]
    print("The dates selected are: " + str(dates[0]) + " to " + str(dates[1]))
    return dates


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Flags for recharge utilities")
    parser.add_argument("--dates", action="store_true")
    parser.add_argument(
        "--start_date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="enter date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--end_date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="enter date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "-r",
        action="store_true",
        help="Overwrite existing recharge folder with new recharge folder",
    )
    parser.add_argument(
        "-upload",
        action="store_true",
        help="Overwrite existing recharge data on Google Drive",
    )
    args = parser.parse_args()

    if not os.path.exists("./rockimagerBacklogs/"):
        os.mkdir("./rockimagerBacklogs/")
    if not os.path.exists("./temp"):
        os.mkdir("./temp")

    dates = []
    if args.start_date and args.end_date:
        dates = [args.start_date, args.end_date]
    if args.dates:
        dates = askForDates()

    if args.r:
        directory = (
            "monthlyRechargesTemp/"
            + str(dates[0])[0:10]
            + "_TO_"
            + str(dates[1])[0:10]
            + "/"
        )
        if os.path.exists(directory):
            subprocess.run(["rm", "-r", directory])

    print("Downloading rockimager log files from Google Drive")
    downloadRockimagerFiles.main(dates)

    print("calculating recharge")
    rechargeSummary = calculateRecharge_auto.main(dates)

    os.system("mv ./temp/*.txt ./rockimagerBacklogs/")
    if args.upload:
        print("appending to collatedRecharge")

        gdrive.appendToCollatedRechargeSheet(rechargeSummary)

        print("uploading to google drive")
        uploadGDriveMonthlyRecharges.main()


if __name__ == "__main__":
    main()
