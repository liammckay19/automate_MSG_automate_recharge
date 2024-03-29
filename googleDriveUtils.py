import pygsheets as pyg
import datetime as dt
import pandas as pd


def authorizeGoogleDriveUsage():
    return pyg.authorize(
        service_file="/Users/liam_msg/Documents/automate_MSG_automate_recharge/pygsheets_api_key.json"
    )


# authorize google drive python
gc = authorizeGoogleDriveUsage()


class UserException(Exception):
    pass


# obtain PI and their use_types from Google drive spreadsheet called Groups
def getPITypes():
    wks_groups = gc.open_by_key("11MoSdyrBc7J1INeGPipwk88Srotjmrh_PbTMxEX49Js").sheet1
    row_data = wks_groups.get_all_values(
        include_tailing_empty=False, include_tailing_empty_rows=False
    )

    coreUsers = []
    associateUsers = []
    regUsers = []
    industryUsers = []

    k = 1  # skip first row
    while k < len(row_data):
        pi, user_type = row_data[k]
        pi = pi.lower()
        if user_type == "regular":
            regUsers.append(pi)
        elif user_type == "associate":
            associateUsers.append(pi)
        elif user_type == "industry":
            industryUsers.append(pi)
        else:
            coreUsers.append(pi)
        k += 1
    print("Core: ", coreUsers)
    print("Associate: ", associateUsers)
    print("Regular: ", regUsers)
    print("Industry: ", industryUsers)
    return [
        coreUsers,
        associateUsers,
        regUsers,
        industryUsers,
        coreUsers + associateUsers + regUsers + industryUsers,
    ]


def getRechargeConst():
    df_rechargeConst = (
        gc.open_by_key("1qOFupGt887mhNfaWiw30lVcBUy2END3cmK9x1MMDYTY")
        .worksheet_by_title("master")
        .get_as_df()
    )
    return df_rechargeConst


# obtain usage log data from Google drive forms/spreadsheets (mosquito, mosquitoLCP, dragonfly)
def getGDriveLogUsage():
    # old xray google drive changed jul 22 2021
    # df_mosquitoLCPLogRAW = gc.open_by_key('1MpwGvh6xlOb4mrn8BtJgs7Fux7hmlZRRdmhBUkhqRAY').sheet1.get_as_df()
    # df_mosquitoLogRAW = gc.open_by_key('1demabrSE50t_euIpP3AhM8V64I3BQuaK1VRcNJCSJmA').sheet1.get_as_df()
    # df_dragonflyLogRAW = gc.open_by_key('1JciEUj4dg1AZedcmi42InLIQs5XINQt5aaok4-vnUwg').sheet1.get_as_df()
    # df_screenOrders = gc.open_by_key('1d6GVWGwwrlh_lTKxVRI08xZSiE__Zieu3WWtwbmOMlE'
    #                                  ).worksheet_by_title('completedOrders').get_as_df()

    df_mosquitoLCPLogRAW = gc.open_by_key(
        "1GWEa5ZRyInx50FEh72tsmht-bcHu5Nl_-ddGQ-FoBZY"
    ).sheet1.get_as_df()
    df_mosquitoLogRAW = gc.open_by_key(
        "18UHYpeEGKw_5LWawPcMiY2VybiCT28BisQ8XsIPR1Pk"
    ).sheet1.get_as_df()
    df_dragonflyLogRAW = gc.open_by_key(
        "1yQ9shuGlHN23iJ2E9lY2la0UKHRMNNvEABGJ1ikP-pE"
    ).sheet1.get_as_df()

    return [df_mosquitoLCPLogRAW, df_mosquitoLogRAW, df_dragonflyLogRAW]


def getGoogleDriveGL():
    return gc.open_by_key(
        "1YI7NFB6JsWugf1c0J4oK7hDHXLM0Oc-wo6bm2pjGHPk"
    ).sheet1.get_as_df()


def getQueriedRechargeByGroup():
    df = (
        gc.open_by_key("1B69agpwT7HMlldmTv9-kkupokVjVU7VS2zX4u59JlZc")
        .worksheet_by_title("largePurchaseRechargeQuery")
        .get_as_df()
    )
    df = df[df.Group != ""]
    return df


def appendToCollatedRechargeSheet(rechargeSummary):
    rechargeSummary = rechargeSummary[
        [
            "Facility Fee",
            "Screens Total Cost",
            "Mosquito Total Cost",
            "RockImager Total Cost",
            "DFly Total Cost",
            "Raw Usage",
            "Usage prop",
            "Month Dist. Cost",
            "Payroll Cost",
            "Use Multiplier",
            "Total Charge",
        ]
    ]
    gc = pyg.authorize(service_file="project-id-3957635354098363168-30ba8b84ccdf.json")
    wks = gc.open_by_key(
        "1B69agpwT7HMlldmTv9-kkupokVjVU7VS2zX4u59JlZc"
    ).worksheet_by_title("collatedRecharge")
    rechargeSummary = rechargeSummary.reset_index()

    rechargeSummary["Month/Year"] = pd.to_datetime(rechargeSummary["Date"])
    rechargeSummary = rechargeSummary.drop("Date", 1)
    rechargeSummary["Month/Year"] = rechargeSummary["Month/Year"] - pd.Timedelta(days=1)

    rechargeSummary["Month/Year"] = rechargeSummary["Month/Year"].dt.strftime("%m | %Y")
    # rechargeSummary = rechargeSummary.drop(columns=["Month/Year"])
    month_year = rechargeSummary.pop("Month/Year")
    rechargeSummary.insert(0, "Month/Year", month_year)
    # rechargeSummary = rechargeSummary.drop(columns=['Date'])
    firstBlankRow = wks.find("", cols=(1, 1), matchEntireCell=True)[0].row
    wks.set_dataframe(
        rechargeSummary, "A" + str(firstBlankRow), copy_index=False, copy_head=False
    )
