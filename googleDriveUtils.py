import pygsheets as pyg

def authorizeGoogleDriveUsage():
    return pyg.authorize(service_file='/Users/liam_msg/Documents/MSG_automate_recharge/msg-Recharge-24378e029f2d.json')

# authorize google drive python
gc = authorizeGoogleDriveUsage()

class UserException(Exception):
    pass

# obtain PI and their use_types from Google drive spreadsheet
def getPITypes():
    wks_groups = gc.open_by_key('1Yom-H6j04TJ5_W1Ic2dlqKsVWrHQbdInQyq_Q7ZVnZA').sheet1
    row_data = wks_groups.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)

    coreUsers = []
    associateUsers = []
    regUsers = []

    k = 1  # skip first row
    while (k < len(row_data)):
        pi, user_type = row_data[k]
        pi = pi.lower()
        if (user_type == 'regular'):
            regUsers.append(pi)
        elif (user_type == 'associate'):
            associateUsers.append(pi)
        else:
            coreUsers.append(pi)
        k += 1
    print(regUsers)
    return [coreUsers, associateUsers, regUsers, coreUsers + associateUsers + regUsers]



def getRechargeConst():
    df_rechargeConst = gc.open_by_key('1d6GVWGwwrlh_lTKxVRI08xZSiE__Zieu3WWtwbmOMlE'
                                      ).worksheet_by_title('master').get_as_df()
    return df_rechargeConst

# obtain usage log data from Google drive forms/spreadsheets (mosquito, mosquitoLCP, dragonfly)
def getGDriveLogUsage():
    df_mosquitoLCPLogRAW = gc.open_by_key('1MpwGvh6xlOb4mrn8BtJgs7Fux7hmlZRRdmhBUkhqRAY').sheet1.get_as_df()
    df_mosquitoLogRAW = gc.open_by_key('1demabrSE50t_euIpP3AhM8V64I3BQuaK1VRcNJCSJmA').sheet1.get_as_df()
    df_dragonflyLogRAW = gc.open_by_key('1JciEUj4dg1AZedcmi42InLIQs5XINQt5aaok4-vnUwg').sheet1.get_as_df()
    df_screenOrders = gc.open_by_key('1d6GVWGwwrlh_lTKxVRI08xZSiE__Zieu3WWtwbmOMlE'
                                     ).worksheet_by_title('completedOrders').get_as_df()

    return [df_mosquitoLCPLogRAW, df_mosquitoLogRAW, df_dragonflyLogRAW, df_screenOrders]


def getGoogleDriveGL():
    return gc.open_by_key('1L610loj5s41wQFYFnzNafI2OeY9kxL0WuPwebtW5k3Q').sheet1.get_as_df()

