import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from inspect import currentframe, getframeinfo


def itemizeDragonflyLog(
    df_dragonflyLog,
    start_date,
    end_date,
    costHDP,
    costSDP,
    costDFlyTip,
    costDFlyReservoir,
    costMXOne,
):

    # Extract relevant data from df_Dragonfly in given date range
    wantedDflyCol = [
        "Group",
        "Name",
        "DFly New Tips",
        "DFly New Reservoirs",
        "DFly New Mixers",
        "DFly New Plates",
        "DFly Plate Type",
    ]
    DFlyUsageMonthByPI = df_dragonflyLog.groupby([pd.Grouper(freq="M"), "Group"])
    DFlyUsageYearByPI = df_dragonflyLog.groupby([df_dragonflyLog.index.year, "Group"])

    itemizedDFlyMonthByPI = DFlyUsageMonthByPI.apply(lambda x: x.head(len(x.index)))[
        wantedDflyCol
    ].loc[start_date:end_date]

    # index = itemizedDFlyMonthByPI.index
    print(itemizedDFlyMonthByPI)
    itemizedDFlyMonthByPI["Cost/plate"] = itemizedDFlyMonthByPI[
        "DFly Plate Type"
    ].apply(lambda x: costHDP if str(x).find("hanging") > 0 else costSDP)
    # itemizedDFlyMonthByPI['Cost/plate'] = pd.Series(itemizedDFlyMonthByPI.index.get_level_values(0)).map(
    #     pd.Series([costHDP if 'hanging' in a else costSDP for a in itemizedDFlyMonthByPI['DFly Plate Type']], index=itemizedDFlyMonthByPI.index.get_level_values(0))).values

    itemizedDFlyMonthByPI["Cost/tip"] = float(costDFlyTip)
    itemizedDFlyMonthByPI["Cost/reservoir"] = float(costDFlyReservoir)
    itemizedDFlyMonthByPI["Cost/mixer"] = float(costMXOne)

    # itemizedDFlyMonthByPI = itemizedDFlyMonthByPI.set_index(index)
    # for r,v in itemizedDFlyMonthByPI.iterrows():
    # print(r,v)
    # reverse index (descending date)
    itemizedDFlyMonthByPI = itemizedDFlyMonthByPI.iloc[::-1]

    # itemizedDFlyMonthByPI = itemizedDFlyMonthByPI.groupby(['Group']).sum()

    # itemizedDFlyMonthByPI = itemizedDFlyMonthByPI.reset_index(drop=False)
    # cols = itemizedDFlyMonthByPI.columns[itemizedDFlyMonthByPI.dtypes.eq('object')]
    # itemizedDFlyMonthByPI[cols] = itemizedDFlyMonthByPI[cols].apply(pd.to_numeric, errors='coerce')

    itemizedDFlyMonthByPI["DFly Total Cost"] = (
        itemizedDFlyMonthByPI["Cost/plate"] * itemizedDFlyMonthByPI["DFly New Plates"]
        + itemizedDFlyMonthByPI["DFly New Mixers"] * float(costMXOne)
        + itemizedDFlyMonthByPI["DFly New Reservoirs"] * float(costDFlyReservoir)
        + itemizedDFlyMonthByPI["DFly New Tips"] * float(costDFlyTip)
    )

    return itemizedDFlyMonthByPI[
        [
            "Group",
            "Name",
            "DFly New Tips",
            "DFly New Reservoirs",
            "DFly New Mixers",
            "DFly New Plates",
            "DFly Plate Type",
            "Cost/tip",
            "Cost/reservoir",
            "Cost/mixer",
            "Cost/plate",
            "DFly Total Cost",
        ]
    ]  # reorganize columns


def itemizeRockimagerLog(
    df_RockImager_1, df_RockImager_2, start_date, end_date, costRockImagerTime
):

    if len(df_RockImager_1.loc[df_RockImager_1["Group"] == "nan"]) > 0:
        print(
            "df_RockImager_1 has nan in Group"
            " <<<<<<<<<<<zzzzz<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        )
    if len(df_RockImager_2.loc[df_RockImager_2["Group"] == "nan"]) > 0:
        print(
            "df_RockImager_2 has nan in Group"
            " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        )

    # print(df_RockImager_2['Group'].fillna(df_RockImager_2['User Name']).value_counts())
    # Extract relevant data from df_RockImager in the given date range
    wantedRockCol = [
        "User Name",
        "Project",
        "Experiment",
        "Plate Type",
        "Rock Dur (min)",
    ]

    rockImagerUsageMonthByPI_1 = df_RockImager_1.groupby(
        [pd.Grouper(freq="M"), "Group"]
    )
    rockImagerUsageYearByPI_1 = df_RockImager_1.groupby(
        [df_RockImager_1.index.year, "Group"]
    )
    itemizedRockMonthByPI_1 = rockImagerUsageMonthByPI_1.apply(
        lambda x: x.head(len(x.index))
    )[wantedRockCol].loc[start_date:end_date]
    itemizedRockMonthByPI_1 = itemizedRockMonthByPI_1[
        (itemizedRockMonthByPI_1["Rock Dur (min)"] > 0.0)
    ]  # remove rows if 'Dur (min)' <= 0
    itemizedRockMonthByPI_1["Cost/min"] = costRockImagerTime
    itemizedRockMonthByPI_1["RockImager Total Cost"] = (
        costRockImagerTime * itemizedRockMonthByPI_1["Rock Dur (min)"]
    )

    # reverse index (descending date)
    itemizedRockMonthByPI_1 = itemizedRockMonthByPI_1.iloc[::-1]

    rockImagerUsageMonthByPI_2 = df_RockImager_2.groupby(
        [pd.Grouper(freq="M"), "Group"]
    )
    rockImagerUsageYearByPI_2 = df_RockImager_2.groupby(
        [df_RockImager_2.index.year, "Group"]
    )
    itemizedRockMonthByPI_2 = rockImagerUsageMonthByPI_2.apply(
        lambda x: x.head(len(x.index))
    )[wantedRockCol].loc[start_date:end_date]

    itemizedRockMonthByPI_2 = itemizedRockMonthByPI_2[
        (itemizedRockMonthByPI_2["Rock Dur (min)"] > 0.0)
    ]  # remove rows if 'Dur (min)' <= 0
    itemizedRockMonthByPI_2["Cost/min"] = costRockImagerTime
    itemizedRockMonthByPI_2["RockImager Total Cost"] = (
        costRockImagerTime * itemizedRockMonthByPI_2["Rock Dur (min)"]
    )

    # reverse index (descending date)
    itemizedRockMonthByPI_2 = itemizedRockMonthByPI_2.iloc[::-1]

    return (
        itemizedRockMonthByPI_1.add(itemizedRockMonthByPI_2),
        itemizedRockMonthByPI_1,
        itemizedRockMonthByPI_2,
    )


def itemizeMosquitoLogs(
    df_mosquitoLog, start_date, end_date, costMosqTip, costHDSConsume, costSDSConsume
):
    # Extract relevant data from df_mosquitoLog in the given date range
    wantedMosqCol = [
        "Group",
        "Name",
        "NumHDP",
        "NumSDP",
        "Mosq Protocol Used",
        "Mosq Tips",
        "Mosq Dur (hr)",
    ]

    mosqUsageMonthByPI = df_mosquitoLog.groupby([pd.Grouper(freq="M"), "Group"])
    print(mosqUsageMonthByPI)
    mosqCrystalUsageYearByPI = df_mosquitoLog.groupby(
        [df_mosquitoLog.index.year, "Group"]
    )

    itemizedMosqCryMonthByPI = mosqUsageMonthByPI.apply(lambda x: x.head(len(x.index)))[
        wantedMosqCol
    ].loc[start_date:end_date]
    # itemizedMosqCryMonthByPI['Group'] = itemizedMosqCryMonthByPI.index

    itemizedMosqCryMonthByPI["Cost/tip"] = float(costMosqTip)
    itemizedMosqCryMonthByPI["Cost/HDSConsume"] = float(costHDSConsume)
    itemizedMosqCryMonthByPI["Cost/SDSConsume"] = float(costSDSConsume)
    print(itemizedMosqCryMonthByPI)
    # itemizedMosqCryMonthByPI = itemizedMosqCryMonthByPI.drop(["Name"])
    itemizedMosqCryMonthByPI["Mosquito Total Cost"] = (
        itemizedMosqCryMonthByPI["Cost/tip"] * itemizedMosqCryMonthByPI["Mosq Tips"]
        + itemizedMosqCryMonthByPI["Cost/HDSConsume"]
        * itemizedMosqCryMonthByPI["NumHDP"]
        + itemizedMosqCryMonthByPI["Cost/SDSConsume"]
        * itemizedMosqCryMonthByPI["NumSDP"]
    )  # needs to be changed eventually

    # reverse index (descending date)
    itemizedMosqCryMonthByPI = itemizedMosqCryMonthByPI.iloc[::-1]
    return itemizedMosqCryMonthByPI


def itemizeScreenOrders(df_screenOrders, start_date, end_date):
    # wantedSOCol = ['Group','Requested By','Item Name','Qty','Unit Price','Screens Total Cost']

    # itemizedSOMonthByPI = df_screenOrders.groupby([pd.Grouper(freq="M"),'Group']).apply(lambda x: x.head(
    #     len(x.index)))[wantedSOCol].loc[start_date:end_date]
    itemizedSOMonthByPI = df_screenOrders
    itemizedSOMonthByPI = itemizedSOMonthByPI[itemizedSOMonthByPI.index <= end_date]
    itemizedSOMonthByPI = itemizedSOMonthByPI[itemizedSOMonthByPI.index >= start_date]
    itemizedSOMonthByPI = itemizedSOMonthByPI.groupby("Group").sum()
    itemizedSOMonthByPI = itemizedSOMonthByPI.iloc[::-1]
    return itemizedSOMonthByPI


def itemizeFacilityFees(
    allUsers,
    coreUsers,
    coreFacilityFee,
    associateUsers,
    assocFacilityFee,
    industryUsers,
    industryFee,
    start_date,
    end_date,
):
    users = []
    usersFee = []
    for user in allUsers:
        if user in coreUsers:
            users.append(user)
            usersFee.append(coreFacilityFee)
        if user in associateUsers:
            users.append(user)
            usersFee.append(assocFacilityFee)
        if user in industryUsers:
            users.append(user)
            usersFee.append(industryFee)

    monthIndex = pd.date_range(start_date, end_date, freq="M")
    numMonths = len(monthIndex)
    lenUsers = len(users)
    users = users * numMonths
    usersFee = usersFee * numMonths
    ind = []
    for m in monthIndex:
        start = datetime(m.year, m.month, 1)  # dummy date
        end = datetime(m.year, m.month, 10)  # dummy date

        td = end - start
        delta = td // len(users)

        for k in range(lenUsers):
            ind.append(start)
            start += delta

    df_facFee = pd.DataFrame(index=ind, columns=["Group", "Facility Fee"])
    df_facFee.index = pd.to_datetime(df_facFee.index)
    df_facFee["Group"] = users
    df_facFee["Facility Fee"] = usersFee
    df_facFee = df_facFee.groupby([pd.Grouper(freq="M"), "Group"]).sum(
        numeric_only=True
    )
    return df_facFee


def findRechargeConstants(df_rechargeConst):
    def findRechargeConst(rowSelector, colSelector):
        return np.float(
            str(
                df_rechargeConst.loc[df_rechargeConst["Item"] == rowSelector][
                    colSelector
                ].values[0]
            )
            .replace("$", "")
            .replace(",", "")
        )

    def findRechargeStr(rowSelector, colSelector):
        return str(
            df_rechargeConst.loc[df_rechargeConst["Item"] == rowSelector][
                colSelector
            ].values[0]
        ).replace("$", "")

    coreMultl = findRechargeConst("Core use multiplier", "Price")
    coreFacilityFee = findRechargeConst("Core facility fee", "Price")  # 650
    assocMult = findRechargeConst("Assoc use multiplier", "Price")
    assocFacilityFee = findRechargeConst("Assoc facility fee", "Price")
    regMult = findRechargeConst("Regular use multiplier", "Price")
    regFacilityFee = findRechargeConst("Regular facility fee", "Price")
    indMult = findRechargeConst("Industry use multiplier", "Price")
    indFacilityFee = findRechargeConst("Industry facility fee", "Price")

    # Get data from facilitySuppliesPricing (https://docs.google.com/spreadsheets/d/1d6GVWGwwrlh_lTKxVRI08xZSiE__Zieu3WWtwbmOMlE/edit#gid=0)
    # greiner 96 well hanging drop plate
    costHDP = findRechargeConst("96-well Greiner Hanging drop plate", "Price/Qty")
    # swis mrc2 96 well sitting drop plate
    costSDP = findRechargeConst("MRC2 Sitting drop plate", "Price/Qty")

    costMosqTip = findRechargeConst("Spool of mosquito tips 9 mm pitch", "Price/Qty")

    costMosquitoTime = findRechargeConst("Mosquito time", "Price")
    costDragonflyTime = findRechargeConst("Dragonfly time", "Price")
    costRockImagerTime = findRechargeConst("RockImager time", "Price")
    costMXOne = findRechargeConst("MXone pin arrays", "Price/Qty")
    costHDSConsume = findRechargeConst(
        "HD Consumables", "Price"
    )  # cost of consumables for mosquito hanging drop plate setup (optical seal, micro reservoirs)
    costSDSConsume = findRechargeConst(
        "SD Consumables", "Price"
    )  # cost of consumables for mosquito sitting drop plate setup (optical seal, micro reservoirs)

    costDFlyReservoir = findRechargeConst("Reservoir dragonfly", "Price/Qty")
    costDFlyTip = findRechargeConst("Pack of 100 dragonfly tips", "Price/Qty")

    # industry specific pricing
    workingCapital = findRechargeConst("working capital", "Price")
    workingCapitalDate = findRechargeStr("working capital", "Description")
    priorYearBalance = findRechargeConst("prior year balance", "Price")
    priorYearBalanceDate = findRechargeStr("prior year balance", "Description")
    totalLabPersonnel = findRechargeConst("total lab personnel", "Qty")
    totalLabPersonnelDate = findRechargeStr("total lab personnel", "Description")
    facilitiesAndAdministrationRate = findRechargeConst(
        "facilities and administration rate", "Price"
    )
    facilitiesAndAdministrationRateDate = findRechargeStr(
        "facilities and administration rate", "Description"
    )

    daysUntilExpired = 365
    expiredFinancialInfo = False
    if datetime.now() >= datetime.strptime(workingCapitalDate, "%m/%d/%Y") + timedelta(
        days=daysUntilExpired
    ):
        print(
            "workingCapital value expired. Please update financial information on"
            " Google Sheets"
        )
        expiredFinancialInfo = True

    if datetime.now() >= datetime.strptime(
        priorYearBalanceDate, "%m/%d/%Y"
    ) + timedelta(days=daysUntilExpired):
        print(
            "priorYearBalance value expired. Please update financial information on"
            " Google Sheets"
        )
        expiredFinancialInfo = True

    if datetime.now() >= datetime.strptime(
        totalLabPersonnelDate, "%m/%d/%Y"
    ) + timedelta(days=daysUntilExpired):
        print(
            "totalLabPersonnel value expired. Please update financial information on"
            " Google Sheets"
        )
        expiredFinancialInfo = True

    if datetime.now() >= datetime.strptime(
        facilitiesAndAdministrationRateDate, "%m/%d/%Y"
    ) + timedelta(days=daysUntilExpired):
        print(
            "facilitiesAndAdministrationRate value expired. Please update financial"
            " information on Google Sheets"
        )
        expiredFinancialInfo = True
    if expiredFinancialInfo:
        exit(1)

    return [
        coreMultl,
        coreFacilityFee,
        assocMult,
        assocFacilityFee,
        regMult,
        regFacilityFee,
        indMult,
        indFacilityFee,
        costHDP,
        costSDP,
        costMosqTip,
        costMosquitoTime,
        costDragonflyTime,
        costRockImagerTime,
        costMXOne,
        costHDSConsume,
        costSDSConsume,
        costDFlyReservoir,
        costDFlyTip,
    ], [
        workingCapital,
        priorYearBalance,
        totalLabPersonnel,
        facilitiesAndAdministrationRate,
    ]


def calculateIndustryRecharge(
    industryUsers, externalRateConstants, outSummary, date_range
):
    (
        workingCapital,
        priorYearBalance,
        totalLabPersonnel,
        facilitiesAndAdministrationRate,
    ) = externalRateConstants
    volume = 1
    unitLabPersonnel = 1
    # External Rate per Month = [(Actual Monthly Expense +1/12 of Working Capital + Prior Year Balance/12) x (Unit Lab Personnel/Total Lab Personnel) + Surplus Revenue] x 26% Facilities & Administration Rate
    # actual monthly expense = (Month Dist. Cost + Mosquito Total Cost + RockImager Total Cost + Large Expense Cost + DFly Total Cost) x Use Multiplier
    # surplus revenue = Screens Total Cost + Payroll Cost + Facility Fee
    print(outSummary)
    outSummary.loc[(slice(None), industryUsers), "Total Charge"] = (
        (
            (
                (
                    outSummary.loc[(slice(None), industryUsers), "Month Dist. Cost"]
                    + outSummary.loc[
                        (slice(None), industryUsers), "Mosquito Total Cost"
                    ]
                    + outSummary.loc[
                        (slice(None), industryUsers), "RockImager Total Cost"
                    ]
                    + outSummary.loc[(slice(None), industryUsers), "Large Expense Cost"]
                    + outSummary.loc[(slice(None), industryUsers), "DFly Total Cost"]
                    * outSummary.loc[(slice(None), industryUsers), "Use Multiplier"]
                )
                + workingCapital / 12
                + priorYearBalance / 12
            )
            * unitLabPersonnel
            / totalLabPersonnel
            + outSummary.loc[(slice(None), industryUsers), "Screens Total Cost"]
            + outSummary.loc[(slice(None), industryUsers), "Payroll Cost"]
            + outSummary.loc[(slice(None), industryUsers), "Facility Fee"]
        )
        * facilitiesAndAdministrationRate
    ) * volume
    outSummary.loc[(slice(None), industryUsers), "workingCapital"] = workingCapital
    outSummary.loc[(slice(None), industryUsers), "priorYearBalance"] = priorYearBalance
    outSummary.loc[(slice(None), industryUsers), "unitLabPersonnel"] = unitLabPersonnel
    outSummary.loc[
        (slice(None), industryUsers), "totalLabPersonnel"
    ] = totalLabPersonnel
    outSummary.loc[
        (slice(None), industryUsers), "facilitiesAndAdministrationRate"
    ] = facilitiesAndAdministrationRate
    outSummary.loc[(slice(None), industryUsers), "volume"] = volume
    return outSummary


def calculateRecharge(dfs, date_range, users):
    start_date, end_date = date_range[0], date_range[1]
    [
        df_mosquitoLog,
        df_mosquitoLCPLog,
        df_dragonflyLog,
        df_RockImager_1,
        df_RockImager_2,
        df_GL,
        df_screenOrders,
        df_rechargeConst,
        df_queriedRechargeByGroup,
    ] = dfs
    [coreUsers, associateUsers, regUsers, industryUsers, allUsers] = users

    (
        coreMultl,
        coreFacilityFee,
        assocMult,
        assocFacilityFee,
        regMult,
        regFacilityFee,
        indMult,
        indFacilityFee,
        costHDP,
        costSDP,
        costMosqTip,
        costMosquitoTime,
        costDragonflyTime,
        costRockImagerTime,
        costMXOne,
        costHDSConsume,
        costSDSConsume,
        costDFlyReservoir,
        costDFlyTip,
    ) = findRechargeConstants(df_rechargeConst)[0]

    itemizedDFlyMonthByPI = itemizeDragonflyLog(
        df_dragonflyLog,
        start_date,
        end_date,
        costHDP,
        costSDP,
        costDFlyTip,
        costDFlyReservoir,
        costMXOne,
    )

    (
        itemizedRockMonthByPI,
        itemizedRockMonthByPI_1,
        itemizedRockMonthByPI_2,
    ) = itemizeRockimagerLog(
        df_RockImager_1, df_RockImager_2, start_date, end_date, costRockImagerTime
    )

    itemizedMosqCryMonthByPI = itemizeMosquitoLogs(
        df_mosquitoLog,
        start_date,
        end_date,
        costMosqTip,
        costHDSConsume,
        costSDSConsume,
    )

    itemizedSOMonthByPI = itemizeScreenOrders(df_screenOrders, start_date, end_date)

    df_facFee = itemizeFacilityFees(
        allUsers,
        coreUsers,
        coreFacilityFee,
        associateUsers,
        assocFacilityFee,
        industryUsers,
        indFacilityFee,
        start_date,
        end_date,
    )

    a = itemizedMosqCryMonthByPI.sum(level=[0, 1], numeric_only=True)[
        ["NumHDP", "NumSDP", "Mosq Tips", "Mosquito Total Cost"]
    ]

    b_1 = itemizedRockMonthByPI_1.sum(level=[0, 1], numeric_only=True)[
        ["Rock Dur (min)", "RockImager Total Cost"]
    ]
    b_2 = itemizedRockMonthByPI_2.sum(level=[0, 1], numeric_only=True)[
        ["Rock Dur (min)", "RockImager Total Cost"]
    ]
    d = itemizedDFlyMonthByPI.sum(level=[0, 1], numeric_only=True)["DFly Total Cost"]
    b = b_1.add(b_2, fill_value=0)

    c = pd.concat([itemizedSOMonthByPI], keys=[a.index.levels[0][0]], names=["Date"])

    monthlyRechargeTotal = pd.concat([a, b, c, d, df_facFee], axis=1).fillna(0)
    monthlyRechargeTotal = monthlyRechargeTotal.reset_index()
    group_index = list(df_queriedRechargeByGroup["Group"])
    date_ = str(monthlyRechargeTotal["level_0"][0].date())
    date_index = [str(monthlyRechargeTotal["level_0"][0].date())] * len(group_index)

    recharge_array_of_index = [date_index, group_index]
    index = pd.MultiIndex.from_arrays(recharge_array_of_index, names=("Date", "Group"))
    # UGLY UGLY CODE that normalizes the average usage proportion of each group
    # totalAvgUsageProportion=sum(list(pd.merge(monthlyRechargeTotal, df_queriedRechargeByGroup[['Group','avg Usage prop']], how='right', on='Group')['avg Usage prop']))
    # monthlyRechargeTotal = monthlyRechargeTotal.reset_index().merge(df_queriedRechargeByGroup[['Group','avg Usage prop']], how='right', on='Group').set_index('index')
    this_month_groups = set(monthlyRechargeTotal["Group"])
    all_groups = set(df_queriedRechargeByGroup["Group"])
    # print(this_month_groups, all_groups)
    groups_to_add = this_month_groups ^ all_groups
    # add in groups that are in df_queriedRechargeByGroup but not in monthlyRechargeTotal

    # for group in groups_to_add:
    #     monthlyRechargeTotal = monthlyRechargeTotal.append(
    #         {'Group': group, 'level_0': monthlyRechargeTotal['level_0'][0]},
    #         ignore_index=True,
    #     )
    # monthlyRechargeTotal = monthlyRechargeTotal.sort_values(by=['Group'])

    # directly match avg usage proportion to the correct group

    # monthlyRechargeTotal['avg Usage prop'] = df_queriedRechargeByGroup[
    #     'general usage proportion'
    # ]
    monthlyRechargeTotal = pd.merge(
        monthlyRechargeTotal,
        df_queriedRechargeByGroup[["Group", "general usage proportion"]],
        on="Group",
        how="left",
    )
    monthlyRechargeTotal = monthlyRechargeTotal.rename(
        columns={"general usage proportion": "avg Usage prop"}
    )

    monthlyRechargeTotal = monthlyRechargeTotal.fillna(0)

    monthlyRechargeTotal["Raw Usage"] = (
        (monthlyRechargeTotal["NumSDP"] * 4 + monthlyRechargeTotal["NumHDP"]) * 10
        + monthlyRechargeTotal["Rock Dur (min)"]
        # + monthlyRechargeTotal['DFly New Plates Set-up'] * 25
    )
    monthlyRechargeTotal = monthlyRechargeTotal.set_index(["level_0", "Group"])
    a1 = monthlyRechargeTotal.groupby(level=[0, 1]).sum().groupby(level=0)

    rawUsagePercent = a1.apply(lambda x: x["Raw Usage"] / x["Raw Usage"].sum())
    rup_t = rawUsagePercent.T
    rup_t.rename(columns={rup_t.columns[0]: "Usage prop"}, inplace=True)
    rup_t = rup_t.reset_index()
    monthlyRechargeTotal = pd.merge(
        monthlyRechargeTotal, rup_t[["Group", "Usage prop"]], on="Group", how="left"
    )
    print(
        "monthlyRechargeTotal usageprop sum to 1 ? = ",
        monthlyRechargeTotal["Usage prop"].sum(),
    )

    df_GL_monthlyExpenses = (
        df_GL[df_GL["Recharge Category"] == "monthlyExpenses"]
        .groupby([pd.Grouper(freq="M")])
        .sum()
        .loc[start_date:end_date]
    )

    df_GL_payroll = (
        df_GL[df_GL["Recharge Category"] == "payroll"]
        .groupby([pd.Grouper(freq="M")])
        .sum()
        .loc[start_date:end_date]
    )

    df_GL_largePayment = (
        df_GL[df_GL["Recharge Category"] == "largePayment"]
        .groupby([pd.Grouper(freq="M")])
        .sum()
        .loc[start_date:end_date]
    )
    # print(monthlyRechargeTotal)

    monthlyRechargeTotal["Use Multiplier"] = regMult

    # Set Use Multiplier column and payments for Core and Assoc users

    monthlyRechargeTotal.loc[
        ((monthlyRechargeTotal["Group"].isin(coreUsers)), "Use Multiplier")
    ] = coreMultl

    monthlyRechargeTotal.loc[
        ((monthlyRechargeTotal["Group"].isin(associateUsers)), "Use Multiplier")
    ] = assocMult

    monthlyRechargeTotal.loc[
        ((monthlyRechargeTotal["Group"].isin(industryUsers)), "Use Multiplier")
    ] = indMult

    # normalize avg Usage prop to sum to 1
    monthlyRechargeTotal["avg Usage prop"] = (
        monthlyRechargeTotal["avg Usage prop"]
        / monthlyRechargeTotal["avg Usage prop"].sum()
    )
    print(
        "(avg usg prop) should be 1.0 = ", monthlyRechargeTotal["avg Usage prop"].sum()
    )
    monthlyRechargeTotal["Date"] = date_
    monthlyRechargeTotal["Date"] = pd.to_datetime(monthlyRechargeTotal["Date"])

    monthlyRechargeTotal = monthlyRechargeTotal.set_index(["Date", "Group"])
    lst_monthlyExpenses = []
    lst_largeExpenses = []
    lst_payroll = []
    for index, row in monthlyRechargeTotal.iterrows():
        if index[0] in df_GL_largePayment.index:
            lst_largeExpenses.append(
                float(row["avg Usage prop"])
                * float(df_GL_largePayment.loc[index[0]]["Actual"].sum())
            )
        else:
            lst_largeExpenses.append(0)

        if index[0] in df_GL_monthlyExpenses.index:
            # calculate how much each lab pays based on their proportion and the distributed expenses
            print(df_GL_monthlyExpenses.loc[index[0]]["Actual"])
            print(row["Usage prop"])
            lst_monthlyExpenses.append(
                row["Usage prop"] * df_GL_monthlyExpenses.loc[index[0]]["Actual"]
            )

            sumMonthFacFee = monthlyRechargeTotal["Facility Fee"].sum()
            diff = df_GL_payroll.loc[index[0]]["Actual"] - sumMonthFacFee
            print("diff of df_GL_payroll.loc[index[0]][Actual] - sumMonthFacFee", diff)
            # print(lst_monthlyExpenses)
            if (
                diff <= 0
            ):  # if total facility fees exceed payroll total, then charge 0 per lab
                diff = 0
            lst_payroll.append(row["Usage prop"] * diff)
            print("price for payroll", row["Usage prop"], diff, "= ", lst_payroll[-1])

        else:
            lst_monthlyExpenses.append(0)
            lst_payroll.append(0)
    monthlyRechargeTotal[
        "Month Dist. Cost"
    ] = lst_monthlyExpenses  # distributed costs include everything except pay-per-use consumables and base salary/benefits
    monthlyRechargeTotal["Payroll Cost"] = lst_payroll
    monthlyRechargeTotal["Large Expense Cost"] = lst_largeExpenses
    print(monthlyRechargeTotal["Large Expense Cost"].sum())
    monthlyRechargeTotal["Total Charge"] = (
        (
            monthlyRechargeTotal["Month Dist. Cost"]
            + monthlyRechargeTotal["Mosquito Total Cost"]
            + monthlyRechargeTotal["RockImager Total Cost"]
            + monthlyRechargeTotal["DFly Total Cost"]
        )
        * monthlyRechargeTotal["Use Multiplier"]
        + monthlyRechargeTotal["Screens Total Cost"]
        + monthlyRechargeTotal["Payroll Cost"]
        + monthlyRechargeTotal["Large Expense Cost"]
        + monthlyRechargeTotal["Facility Fee"]
    )

    outSummary = monthlyRechargeTotal[
        [
            "Facility Fee",
            "Screens Total Cost",
            "Mosquito Total Cost",
            "RockImager Total Cost",
            "DFly Total Cost",
            "Raw Usage",
            "Usage prop",
            "avg Usage prop",
            "Month Dist. Cost",
            "Large Expense Cost",
            "Payroll Cost",
            "Use Multiplier",
            "Total Charge",
        ]
    ]
    outSummary = calculateIndustryRecharge(
        industryUsers=industryUsers,
        externalRateConstants=findRechargeConstants(df_rechargeConst)[1],
        outSummary=outSummary,
        date_range=date_range,
    )

    outSummary.index.set_names(names="Group", level=1, inplace=True)
    outSummary = outSummary.sort_index(ascending=False)

    daterange = str(start_date)[0:10] + "_TO_" + str(end_date)[0:10]
    fileOut = [
        "mosquitoUsage" + daterange,
        "4c_rockImagerUsage" + daterange,
        "20c_rockImagerUsage" + daterange,
        "dragonflyUsage" + daterange,
        "screenOrders" + daterange,
    ]

    itemizedMosqCryMonthByPI.index.set_levels(
        itemizedMosqCryMonthByPI.index.levels[2].strftime("%m/%d/%Y %H:%M:%S"),
        level=2,
        inplace=True,
        verify_integrity=False,
    )
    itemizedRockMonthByPI_1.index.set_levels(
        itemizedRockMonthByPI_1.index.levels[2].strftime("%m/%d/%Y %H:%M:%S"),
        level=2,
        inplace=True,
        verify_integrity=False,
    )
    itemizedRockMonthByPI_2.index.set_levels(
        itemizedRockMonthByPI_2.index.levels[2].strftime("%m/%d/%Y %H:%M:%S"),
        level=2,
        inplace=True,
        verify_integrity=False,
    )
    itemizedDFlyMonthByPI.index.set_levels(
        itemizedDFlyMonthByPI.index.levels[2].strftime("%m/%d/%Y %H:%M:%S"),
        level=2,
        inplace=True,
        verify_integrity=False,
    )
    wantedSOCol = [
        "Group",
        "Requested By",
        "Item Name",
        "Qty",
        "Unit Price",
        "Screens Total Cost",
    ]

    itemizedSOMonthByPI = (
        df_screenOrders.groupby([pd.Grouper(freq="M"), "Group"])
        .apply(lambda x: x.head(len(x.index)))[wantedSOCol]
        .loc[start_date:end_date]
    )
    itemizedSOMonthByPI = itemizedSOMonthByPI.iloc[::-1]

    itemizedSOMonthByPI.index.set_levels(
        itemizedSOMonthByPI.index.levels[2].strftime("%m/%d/%Y %H:%M:%S").values,
        level=2,
        inplace=True,
        verify_integrity=False,
    )

    dfOut = [
        itemizedMosqCryMonthByPI,
        itemizedRockMonthByPI_1,
        itemizedRockMonthByPI_2,
        itemizedDFlyMonthByPI,
        itemizedSOMonthByPI,
    ]
    # print(itemizedRockMonthByPI_1)
    # print(itemizedRockMonthByPI_2)
    return outSummary, fileOut, dfOut
