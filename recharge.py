import pandas as pd
import numpy as np
from datetime import datetime


def itemizeDragonflyLog(df_dragonflyLog, start_date, end_date, costHDP, costSDP, costDFlyTip, costDFlyReservoir,
                        costMXOne):
    # Extract relevant data from df_Dragonfly in given date range
    wantedDflyCol = ['Group', 'Name', 'DFly New Tips', 'DFly New Reservoirs', 'DFly New Mixers', 'DFly New Plates',
                     'DFly Plate Type']
    DFlyUsageMonthByPI = df_dragonflyLog.groupby([pd.Grouper(freq="M"), 'Group'])
    DFlyUsageYearByPI = df_dragonflyLog.groupby([df_dragonflyLog.index.year, 'Group'])

    itemizedDFlyMonthByPI = DFlyUsageMonthByPI.apply(lambda x: x.head(
        len(x.index)))[wantedDflyCol].loc[start_date:end_date]
    itemizedDFlyMonthByPI['Cost/plate'] = itemizedDFlyMonthByPI['DFly Plate Type'].apply(lambda x: costHDP if x.find(
        'hanging') > 0 else costSDP)  # NEEDS to be changed for price for specific plate type
    itemizedDFlyMonthByPI['Cost/tip'] = costDFlyTip
    itemizedDFlyMonthByPI['Cost/reservoir'] = costDFlyReservoir
    itemizedDFlyMonthByPI['Cost/mixer'] = costMXOne
    itemizedDFlyMonthByPI = itemizedDFlyMonthByPI.iloc[::-1]  # reverse index (descending date)

    itemizedDFlyMonthByPI['DFly Total Cost'] = itemizedDFlyMonthByPI['Cost/plate'] * itemizedDFlyMonthByPI[
        'DFly New Plates'] \
                                               + itemizedDFlyMonthByPI['DFly New Mixers'] * costMXOne + \
                                               itemizedDFlyMonthByPI['DFly New Reservoirs'] * costDFlyReservoir \
                                               + itemizedDFlyMonthByPI['DFly New Tips'] * costDFlyTip

    return itemizedDFlyMonthByPI[
        ['Group', 'Name', 'DFly New Tips', 'DFly New Reservoirs', 'DFly New Mixers',
         'DFly New Plates', 'DFly Plate Type', 'Cost/tip', 'Cost/reservoir', 'Cost/mixer', 'Cost/plate',
         'DFly Total Cost']]  # reorganize columns


def itemizeRockimagerLog(df_RockImager_1, df_RockImager_2, start_date, end_date, costRockImagerTime):
    # Extract relevant data from df_RockImager in the given date range
    wantedRockCol = ['User Name', 'Project', 'Experiment', 'Plate Type', 'Rock Dur (min)']

    rockImagerUsageMonthByPI_1 = df_RockImager_1.groupby([pd.Grouper(freq="M"), 'Group'])
    rockImagerUsageYearByPI_1 = df_RockImager_1.groupby([df_RockImager_1.index.year, 'Group'])
    itemizedRockMonthByPI_1 = rockImagerUsageMonthByPI_1.apply(lambda x: x.head(
        len(x.index)))[wantedRockCol].loc[start_date:end_date]

    itemizedRockMonthByPI_1 = itemizedRockMonthByPI_1[
        (itemizedRockMonthByPI_1['Rock Dur (min)'] > 0)]  # remove rows if 'Dur (min)' <= 0
    itemizedRockMonthByPI_1['Cost/min'] = costRockImagerTime
    itemizedRockMonthByPI_1['RockImager Total Cost'] = costRockImagerTime * itemizedRockMonthByPI_1['Rock Dur (min)']

    itemizedRockMonthByPI_1 = itemizedRockMonthByPI_1.iloc[::-1]  # reverse index (descending date)

    rockImagerUsageMonthByPI_2 = df_RockImager_2.groupby([pd.Grouper(freq="M"), 'Group'])
    rockImagerUsageYearByPI_2 = df_RockImager_2.groupby([df_RockImager_2.index.year, 'Group'])
    itemizedRockMonthByPI_2 = rockImagerUsageMonthByPI_2.apply(lambda x: x.head(
        len(x.index)))[wantedRockCol].loc[start_date:end_date]

    itemizedRockMonthByPI_2 = itemizedRockMonthByPI_2[
        (itemizedRockMonthByPI_2['Rock Dur (min)'] > 0)]  # remove rows if 'Dur (min)' <= 0
    itemizedRockMonthByPI_2['Cost/min'] = costRockImagerTime
    itemizedRockMonthByPI_2['RockImager Total Cost'] = costRockImagerTime * itemizedRockMonthByPI_2['Rock Dur (min)']

    itemizedRockMonthByPI_2 = itemizedRockMonthByPI_2.iloc[::-1]  # reverse index (descending date)

    return itemizedRockMonthByPI_1.add(itemizedRockMonthByPI_2), itemizedRockMonthByPI_1, itemizedRockMonthByPI_2


def itemizeMosquitoLogs(df_mosquitoLog, start_date, end_date, costMosqTip, costHDSConsume, costSDSConsume):
    # Extract relevant data from df_mosquitoLog in the given date range
    wantedMosqCol = ['Name', 'NumHDP', 'NumSDP', 'Mosq Protocol Used', 'Mosq Tips', 'Mosq Dur (hr)']

    mosqUsageMonthByPI = df_mosquitoLog.groupby([pd.Grouper(freq="M"), 'Group'])
    mosqCrystalUsageYearByPI = df_mosquitoLog.groupby([df_mosquitoLog.index.year, 'Group'])
    itemizedMosqCryMonthByPI = mosqUsageMonthByPI.apply(lambda x: x.head(
        len(x.index)))[wantedMosqCol].loc[start_date:end_date]

    itemizedMosqCryMonthByPI['Cost/tip'] = costMosqTip

    itemizedMosqCryMonthByPI['Mosquito Total Cost'] = costMosqTip * itemizedMosqCryMonthByPI['Mosq Tips'] \
                                                      + costHDSConsume * itemizedMosqCryMonthByPI[
                                                          'NumHDP'] + costSDSConsume * itemizedMosqCryMonthByPI[
                                                          'NumSDP']  # needs to be changed eventually

    itemizedMosqCryMonthByPI = itemizedMosqCryMonthByPI.iloc[::-1]  # reverse index (descending date)
    return itemizedMosqCryMonthByPI


def itemizeScreenOrders(df_screenOrders, start_date, end_date):
    # wantedSOCol = ['Group','Requested By','Item Name','Qty','Unit Price','Screens Total Cost']

    # itemizedSOMonthByPI = df_screenOrders.groupby([pd.Grouper(freq="M"),'Group']).apply(lambda x: x.head(
    #     len(x.index)))[wantedSOCol].loc[start_date:end_date]
    itemizedSOMonthByPI = df_screenOrders
    itemizedSOMonthByPI = itemizedSOMonthByPI[itemizedSOMonthByPI.index <= end_date]
    itemizedSOMonthByPI = itemizedSOMonthByPI[itemizedSOMonthByPI.index >= start_date]
    itemizedSOMonthByPI = itemizedSOMonthByPI.groupby('Group').sum()
    itemizedSOMonthByPI = itemizedSOMonthByPI.iloc[::-1]
    return itemizedSOMonthByPI


def itemizeFacilityFees(allUsers, coreUsers, coreFacilityFee, associateUsers, assocFacilityFee, start_date, end_date):
    users = []
    usersFee = []
    for user in allUsers:
        if user in coreUsers:
            users.append(user)
            usersFee.append(coreFacilityFee)
        if user in associateUsers:
            users.append(user)
            usersFee.append(assocFacilityFee)

    monthIndex = pd.date_range(start_date, end_date, freq='M')
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

    df_facFee = pd.DataFrame(index=ind, columns=['Group', 'Facility Fee'])
    df_facFee.index = pd.to_datetime(df_facFee.index)
    df_facFee['Group'] = users
    df_facFee['Facility Fee'] = usersFee
    df_facFee = df_facFee.groupby([pd.Grouper(freq="M"), 'Group']).sum(level=[0, 1], numeric_only=True)
    return df_facFee


def findRechargeConstants(df_rechargeConst):
    def findRechargeConst(rowSelector, colSelector):
        return np.float(df_rechargeConst.loc[df_rechargeConst['Item'] == rowSelector][colSelector] \
                        .values[0].replace('$', '', ))

    coreMultl = findRechargeConst("Core use multiplier", "Price")
    coreFacilityFee = findRechargeConst('Core facility fee', 'Price')  # 650
    assocMult = findRechargeConst('Assoc use multiplier', 'Price')
    assocFacilityFee = findRechargeConst('Assoc facility fee', 'Price')
    regMult = findRechargeConst('Regular use multiplier', 'Price')
    regFacilityFee = findRechargeConst('Regular facility fee', 'Price')

    # Get data from facilitySuppliesPricing (https://docs.google.com/spreadsheets/d/1d6GVWGwwrlh_lTKxVRI08xZSiE__Zieu3WWtwbmOMlE/edit#gid=0)
    costHDP = findRechargeConst('96-well Greiner Hanging drop plate', 'Price/Qty')  # greiner 96 well hanging drop plate
    costSDP = findRechargeConst('MRC2 Sitting drop plate', 'Price/Qty')  # swis mrc2 96 well sitting drop plate

    costMosqTip = findRechargeConst('Spool of mosquito tips 9 mm pitch', 'Price/Qty')

    costMosquitoTime = findRechargeConst('Mosquito time', 'Price')
    costDragonflyTime = findRechargeConst('Dragonfly time', 'Price')
    costRockImagerTime = findRechargeConst('RockImager time', 'Price')
    costMXOne = findRechargeConst('MXone pin arrays', 'Price/Qty')
    costHDSConsume = findRechargeConst('HD Consumables',
                                       'Price')  # cost of consumables for mosquito hanging drop plate setup (optical seal, micro reservoirs)
    costSDSConsume = findRechargeConst('SD Consumables',
                                       'Price')  # cost of consumables for mosquito sitting drop plate setup (optical seal, micro reservoirs)

    costDFlyReservoir = findRechargeConst('Reservoir dragonfly', 'Price/Qty')
    costDFlyTip = findRechargeConst('Pack of 100 dragonfly tips', 'Price/Qty')
    return [coreMultl, coreFacilityFee, assocMult, assocFacilityFee, regMult, regFacilityFee, costHDP, costSDP,
            costMosqTip, costMosquitoTime, costDragonflyTime, costRockImagerTime, costMXOne, costHDSConsume,
            costSDSConsume, costDFlyReservoir, costDFlyTip]


def calculateRecharge(dfs, date_range, users):
    start_date, end_date = date_range[0], date_range[1]
    [df_mosquitoLog, df_mosquitoLCPLog, df_dragonflyLog, df_RockImager_1,
     df_RockImager_2, df_GL, df_screenOrders, df_rechargeConst] = dfs
    [coreUsers, associateUsers, regUsers, allUsers] = users

    coreMultl, coreFacilityFee, assocMult, assocFacilityFee, regMult, regFacilityFee, costHDP, costSDP, \
    costMosqTip, costMosquitoTime, costDragonflyTime, costRockImagerTime, costMXOne, costHDSConsume, costSDSConsume, \
    costDFlyReservoir, costDFlyTip = findRechargeConstants(df_rechargeConst)

    itemizedDFlyMonthByPI = itemizeDragonflyLog(df_dragonflyLog, start_date, end_date, costHDP, costSDP, costDFlyTip,
                                                costDFlyReservoir,
                                                costMXOne)

    itemizedRockMonthByPI, itemizedRockMonthByPI_1, itemizedRockMonthByPI_2 = itemizeRockimagerLog(df_RockImager_1,
                                                                                                   df_RockImager_2,
                                                                                                   start_date, end_date,
                                                                                                   costRockImagerTime)

    itemizedMosqCryMonthByPI = itemizeMosquitoLogs(df_mosquitoLog, start_date, end_date, costMosqTip, costHDSConsume,
                                                   costSDSConsume)

    itemizedSOMonthByPI = itemizeScreenOrders(df_screenOrders, start_date, end_date)

    df_facFee = itemizeFacilityFees(allUsers, coreUsers, coreFacilityFee, associateUsers, assocFacilityFee, start_date,
                                    end_date)

    a = itemizedMosqCryMonthByPI.sum(level=[0, 1], numeric_only=True)[
        ['NumHDP', 'NumSDP', 'Mosq Tips', 'Mosquito Total Cost']]

    b_1 = itemizedRockMonthByPI_1.sum(level=[0, 1], numeric_only=True)[['Rock Dur (min)', 'RockImager Total Cost']]
    b_2 = itemizedRockMonthByPI_2.sum(level=[0, 1], numeric_only=True)[['Rock Dur (min)', 'RockImager Total Cost']]
    d = itemizedDFlyMonthByPI.sum(level=[0, 1], numeric_only=True)['DFly Total Cost']
    b = (b_1.add(b_2, fill_value=0))

    c = pd.concat([itemizedSOMonthByPI], keys=[a.index.levels[0][0]], names=['Date'])

    monthlyRechargeTotal = pd.concat([a, b, c, d, df_facFee], axis=1).fillna(0)
    monthlyRechargeTotal['Raw Usage'] = (monthlyRechargeTotal['NumSDP'] + monthlyRechargeTotal['NumHDP']) * 10 \
                                        + monthlyRechargeTotal['Rock Dur (min)']
    # + monthlyRechargeTotal['Rock Dur (min)'] + monthlyRechargeTotal['DFly New Plates Set-up']*25 #might need to redefine to better definition

    a1 = monthlyRechargeTotal.groupby(level=[0, 1]).sum().groupby(level=0)

    rawUsagePercent = a1.apply(lambda x: x['Raw Usage'] / x['Raw Usage'].sum())
    monthlyRechargeTotal['Usage prop'] = pd.Series.ravel(rawUsagePercent)

    df_GL_monthlyExpenses = df_GL[df_GL['Recharge Category'] == 'monthlyExpenses'].groupby(
        [pd.Grouper(freq="M")]).sum().loc[start_date:end_date]

    df_GL_payroll = df_GL[df_GL['Recharge Category'] == 'payroll'].groupby(
        [pd.Grouper(freq="M")]).sum().loc[start_date:end_date]

    monthlyRechargeTotal['Use Multiplier'] = regMult

    # Set Use Multiplier column and payments for Core and Assoc users
    monthlyRechargeTotal.loc[((monthlyRechargeTotal.index.levels[0],
                               coreUsers), 'Use Multiplier')] = coreMultl

    monthlyRechargeTotal.loc[((monthlyRechargeTotal.index.levels[0],
                               associateUsers), 'Use Multiplier')] = assocMult

    lst_monthlyExpenses = []
    lst_payroll = []
    for index, row in monthlyRechargeTotal.iterrows():
        if (index[0] in df_GL_monthlyExpenses.index):
            # calculate how much each lab pays based on their proportion and the distributed expenses
            lst_monthlyExpenses.append(row['Usage prop'] * df_GL_monthlyExpenses.loc[index[0]]['Actual'])
            sumMonthFacFee = monthlyRechargeTotal.loc[index[0]]['Facility Fee'].sum()
            diff = df_GL_payroll.loc[index[0]]['Actual'] - sumMonthFacFee
            print(lst_monthlyExpenses)
            if (diff <= 0):  # if total facility fees exceed payroll total, then charge 0 per lab
                diff = 0
            lst_payroll.append(row['Usage prop'] * diff)
        else:
            lst_monthlyExpenses.append(0)
            lst_payroll.append(0)

    monthlyRechargeTotal[
        'Month Dist. Cost'] = lst_monthlyExpenses  # distributed costs include everything except pay-per-use consumables and base salary/benefits
    monthlyRechargeTotal['Payroll Cost'] = lst_payroll
    monthlyRechargeTotal['Total Charge'] = \
        (monthlyRechargeTotal['Month Dist. Cost'] + monthlyRechargeTotal['Mosquito Total Cost'] + monthlyRechargeTotal['RockImager Total Cost'] + monthlyRechargeTotal['DFly Total Cost']) \
            * monthlyRechargeTotal['Use Multiplier'] \
            + monthlyRechargeTotal['Screens Total Cost'] \
            + monthlyRechargeTotal['Payroll Cost'] \
            + monthlyRechargeTotal['Facility Fee']


    outSummary = monthlyRechargeTotal[
        ['Facility Fee', 'Screens Total Cost', 'Mosquito Total Cost', 'RockImager Total Cost', 'DFly Total Cost',
         'Raw Usage', 'Usage prop', 'Month Dist. Cost', 'Payroll Cost', 'Use Multiplier', 'Total Charge']]
    outSummary.index.set_names(names='Group', level=1, inplace=True)
    outSummary = outSummary.sort_index(ascending=False)
    daterange = str(start_date)[0:10] + '_TO_' + str(end_date)[0:10]
    fileOut = ['mosquitoUsage' + daterange, '4c_rockImagerUsage' + daterange,
               '20c_rockImagerUsage' + daterange, 'dragonflyUsage' + daterange, 'screenOrders' + daterange]

    itemizedMosqCryMonthByPI.index.set_levels(itemizedMosqCryMonthByPI
                                              .index.levels[2].strftime('%m/%d/%Y %H:%M:%S'), level=2, inplace=True,
                                              verify_integrity=False)
    itemizedRockMonthByPI_1.index.set_levels(itemizedRockMonthByPI_1
                                             .index.levels[2].strftime('%m/%d/%Y %H:%M:%S'), level=2, inplace=True,
                                             verify_integrity=False)
    itemizedRockMonthByPI_2.index.set_levels(itemizedRockMonthByPI_2
                                             .index.levels[2].strftime('%m/%d/%Y %H:%M:%S'), level=2, inplace=True,
                                             verify_integrity=False)
    itemizedDFlyMonthByPI.index.set_levels(itemizedDFlyMonthByPI
                                           .index.levels[2].strftime('%m/%d/%Y %H:%M:%S'), level=2, inplace=True,
                                           verify_integrity=False)
    wantedSOCol = ['Group', 'Requested By', 'Item Name', 'Qty', 'Unit Price', 'Screens Total Cost']

    itemizedSOMonthByPI = df_screenOrders.groupby([pd.Grouper(freq="M"), 'Group']).apply(lambda x: x.head(
        len(x.index)))[wantedSOCol].loc[start_date:end_date]
    itemizedSOMonthByPI = itemizedSOMonthByPI.iloc[::-1]

    itemizedSOMonthByPI.index.set_levels(
        itemizedSOMonthByPI.index.levels[2].strftime('%m/%d/%Y %H:%M:%S').values,
        level=2,
        inplace=True, verify_integrity=False)

    dfOut = [itemizedMosqCryMonthByPI, itemizedRockMonthByPI_1,
             itemizedRockMonthByPI_2, itemizedDFlyMonthByPI, itemizedSOMonthByPI]
    print(itemizedRockMonthByPI_1)
    print(itemizedRockMonthByPI_2)
    return outSummary, fileOut, dfOut
