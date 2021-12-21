import sys
import subprocess
import os
import pandas as pd
import pygsheets as pyg
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date, timedelta
from tkinter.filedialog import askopenfilename
import shutil
import glob

import googleDriveUtils as gdrive
import cleanData as clean
import recharge as recharge
from grab_pyanywhere_orders import (
    get_orders_df_from_xtalscreenorder_pythonanywhere_website as get_xtalscreenorders,
)

# authorize google drive python
gc = gdrive.authorizeGoogleDriveUsage()


class UserException(Exception):
    pass


# obtain usage log data from Google drive forms/spreadsheets (mosquito, mosquitoLCP, dragonfly)
def getGDriveLogUsage(dates):

    # screen order site changed to xtalscreenorder june 19
    (
        df_mosquitoLCPLogRAW,
        df_mosquitoLogRAW,
        df_dragonflyLogRAW,
    ) = gdrive.getGDriveLogUsage()
    df_screenOrders = get_xtalscreenorders()
    # print(df_screenOld.columns)
    # print(df_screenOrders.columns)

    df_mosquitoLCPLog = clean.clean_DF_MosquitoLCP(df_mosquitoLCPLogRAW, dates)
    df_mosquitoLog = clean.clean_DF_MosquitoCrystal(df_mosquitoLogRAW, dates)
    df_dragonflyLog = clean.clean_DF_Dragonfly(df_dragonflyLogRAW, dates)
    df_screenOrdersLog = clean.clean_DF_screenOrders(df_screenOrders, dates)
    return [df_mosquitoLog, df_mosquitoLCPLog, df_dragonflyLog, df_screenOrdersLog]


def getRockImagerUsage(dates, filename=None):
    start_date, end_date = dates

    if filename:
        path = filename
        try:
            if filename.endswith(".tsv"):
                df = pd.read_csv(path, delimiter="\t")
            elif filename.endswith(".txt"):
                df = pd.read_csv(path, delimiter="\t")
            elif filename.endswith(".csv"):
                df = pd.read_csv(path, delimiter=",")
            else:
                raise UserException
        except UserException as e:
            print("\nWrong file type selected (ONLY .csv or .tsv files)")
            exit()

    print("\nSelected:\n" + filename + "\n")
    # MAIN SCRIPT BELOW
    # Remove "groups" not in recharge system (administrators, etc.)
    # df = df[df['Group'] != 'Administrators']
    null_row = [
        [
            start_date,
            "Plate Move - Imager to Stage",
            0,
            0,
            "null_plate",
            "Plate Movement",
            0,
            "null_protein",
            "null_screen",
            "null_user",
            0,
            "0 minute",
        ]
    ]
    df = df.append(
        pd.DataFrame(
            null_row,
            columns=[
                "Time",
                "Event Type",
                "Plate ID",
                "Insp. ID",
                "Plate Type",
                "Light Path",
                "Setting",
                "Project",
                "Experiment",
                "User Name",
                "Group",
                "Duration",
            ],
        )
    )
    # Look at 'Duration' column and extract numerical data inplace
    durStr = "Rock Dur (min)"
    df.rename(columns={"Duration": durStr}, inplace=True)
    df[durStr] = df[durStr].str.replace(r"[^0-9.]", "", regex=True).astype("float")

    # Look at 'Time' column and convert to datetime type
    df.index = pd.to_datetime(df.pop("Time"))  # Change index to datetime index
    df = df[df.index.notnull()]
    mask = (df.index >= start_date) & (df.index <= end_date)
    df = df.loc[mask]
    df["Group"] = (
        df["Group"].astype(str).map(lambda s: s.lower())
    )  # make group name lowercase to standardize

    def removeNaN_FromRockImagerLog(row):
        if row["Group"] == "nan":
            if row["User Name"] == "lin":
                return "remegen biosciences"
            elif row["User Name"] == "QCRG":
                return "qcrg"
        else:
            return row["Group"]

    df["Group"] = df.apply(lambda row: removeNaN_FromRockImagerLog(row), axis=1)
    return df


def getGL(dates):
    df = gdrive.getGoogleDriveGL()

    df["Actual"] = pd.to_numeric(df["Actual"], errors="coerce").fillna(0)

    start_date, end_date = dates

    # categories of charges; should be lower case
    amortizedExpenses = ["voucher"]
    voucherExceptions = [
        "airgas",
        "vpl",
        "vantage point logistics",
        "cdw-government",
        "distributed-exception",
    ]
    monthlyExpenses = ["recharge"]
    largeExpenses = ["largepayment"]
    payroll = ["payroll"]

    # checks if strings of lst1 is a substring of any string in lst2 and returns array of bool
    def substringInListOfStrings(x, lst):
        for s in lst:
            if x.find(s) > -1:
                return True
        return False

    df.index = pd.to_datetime(df.pop("JrnlDate"))
    mask = (df.index >= start_date) & (df.index <= end_date)
    # df = df.loc[start_date:end_date]
    df = df.loc[mask]
    # try:
    lst_rechargeCategory = []
    for index, row in df.iterrows():
        s = row[["TrnsTyp", "Description"]]
        if substringInListOfStrings(
            str(s[0]).lower(), amortizedExpenses
        ) and not substringInListOfStrings(str(s[1]).lower(), voucherExceptions):
            lst_rechargeCategory.append("amortizedExpenses")
        elif substringInListOfStrings(str(s[0]).lower(), payroll):
            lst_rechargeCategory.append("payroll")
        elif substringInListOfStrings(str(s[0]).lower(), largeExpenses):
            lst_rechargeCategory.append("largePayment")
        else:
            lst_rechargeCategory.append("monthlyExpenses")

    df["Recharge Category"] = lst_rechargeCategory
    # df['Recharge Category'] = df[['TrnsTyp', 'Description']].apply(lambda s: 'amortizedExpenses'
    # if substringInListOfStrings(str(s[0]).lower(), amortizedExpenses) and not (substringInListOfStrings(str(s[1]).lower(), voucherExceptions)) \
    #     else ('payroll' if substringInListOfStrings(str(s[0]).lower(), payroll)
    #     else ('monthlyExpenses' if substringInListOfStrings(str(s[0]).lower(), monthlyExpenses)
    #           else 'monthlyExpenses'), axis=1)
    # except ValueError:
    #     print("Dates not found for GL. Run script on collatedGL_DPE")
    #     exit(0)
    return df


# Make the output files more Excel friendly
# assumes index in TimeStamp format categorized by month (level -0)
def makeExcelFriendly(df):
    df.index.set_names(["Month/Year"], [0], inplace=True)
    print(df)
    df.index.set_levels(
        df.index.levels[0].strftime("%m/%Y"),
        level=0,
        inplace=True,
        verify_integrity=False,
    )
    return df


# takes df and output path w/ specified fileExt
def exportToFile(df, pth, fileExt=".xlsx"):
    if not (fileExt == ".xlsx" or fileExt == ".csv"):
        print("fileExt needs to be '.csv' or '.xlsx'")
    else:
        if fileExt == ".csv":
            df.to_csv(pth + fileExt)
        else:
            df.to_excel(pth + fileExt, freeze_panes=(1, 1))

        # assume df_lst is a list multi-index df with 'Group' level = 1


def getFilesByPI(df_lst, pth_lst, PI_lst, direc):
    for df, pth in zip(df_lst, pth_lst):
        for PI in PI_lst:
            bools = df.index.get_level_values("Group") == PI
            if any(bools):
                a = df.loc[bools]
                pi_folder = direc + PI + "/"

                if not os.path.exists(pi_folder):
                    os.makedirs(pi_folder)

                exportToFile(makeExcelFriendly(a), pi_folder + pth)


# takes in currency as str and converts to float
def currencyToFloat(s):
    return np.float(s.replace("$", ""))


def getCellByRowCol(df, rowHeader, rowSelector, colSelector):
    return df.loc[df[rowHeader] == rowSelector][colSelector].to_numpy()[0]


def main(override_dates=[]):
    coldFile = glob.glob("./temp/20c*")[0]
    roomFile = glob.glob("./temp/4c*")[0]

    if override_dates:
        start_date = override_dates[0]
        end_date = override_dates[1]
        dates = [str(override_dates[0]), str(override_dates[1])]
    else:
        # calculate start and end dates
        start_date, end_date = "", ""
        date_for_recharge = date.today()

        end_d = date_for_recharge.replace(day=1)
        start_d = end_d - timedelta(days=1)
        start_d = start_d.replace(day=1)

        start_date = datetime.strptime(str(start_d), "%Y-%m-%d")
        end_date = datetime.strptime(str(end_d) + "-23-59-59", "%Y-%m-%d-%H-%M-%S")

        dates = [str(start_date), str(end_date)]
    print("The dates selected are: " + dates[0] + " to " + dates[1])
    coreUsers, associateUsers, regUsers, indUsers, allUsers = gdrive.getPITypes()
    (
        df_mosquitoLog,
        df_mosquitoLCPLog,
        df_dragonflyLog,
        df_screenOrders,
    ) = getGDriveLogUsage(dates)
    df_RockImager_1 = getRockImagerUsage(dates, coldFile)
    df_RockImager_2 = getRockImagerUsage(dates, roomFile)
    df_GL = getGL(dates)
    df_rechargeConst = gdrive.getRechargeConst()
    df_queriedRechargeByGroup = gdrive.getQueriedRechargeByGroup()
    dfs_input = [
        df_mosquitoLog,
        df_mosquitoLCPLog,
        df_dragonflyLog,
        df_RockImager_1,
        df_RockImager_2,
        df_GL,
        df_screenOrders,
        df_rechargeConst,
        df_queriedRechargeByGroup,
    ]
    # for df in dfs_input:
    #     print(df.head())
    users = [coreUsers, associateUsers, regUsers, indUsers, allUsers]
    rechargeSummary, fileOut_lst, dfOut_lst = recharge.calculateRecharge(
        dfs_input, [start_date, end_date], users
    )
    print(rechargeSummary)
    directory = (
        "monthlyRechargesTemp/"
        + str(start_date)[0:10]
        + "_TO_"
        + str(end_date)[0:10]
        + "/"
    )
    if not os.path.exists(directory):
        os.makedirs(directory)
        getFilesByPI(dfOut_lst, fileOut_lst, allUsers, directory)
        exportToFile(
            makeExcelFriendly(rechargeSummary),
            directory
            + "rechargeSummary"
            + str(start_date)[0:10]
            + "_TO_"
            + str(end_date)[0:10],
        )
        print("saved in ", directory)
    subprocess.run(["open " + directory], shell=True)
    return rechargeSummary


if __name__ == "__main__":
    main()
