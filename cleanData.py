import pandas as pd

def clean_DF_MosquitoCrystal(df, dates):
    start_date, end_date = dates
    # Rename columns to make easier to read, NEED TO CHANGE IF CHANGES MADE IN GOOGLE FORM
    df.rename(columns={'How many tips did you use in total?': 'Mosq Tips',
                       'How many plates did you set up?': 'Mosq Plates Set-up',
                       'How many sitting drop plates did you set up? (Enter 0 if none)': 'NumSDP',
                       'How many hanging drop plates did you set up? (Enter 0 if none)': 'NumHDP',
                       'What is your name?': 'Name',
                       'Which lab are you from?': 'Group',
                       'Did you use your own plates or those from the common supply?': 'Source of plates',
                       'What day did you use the Mosquito?': 'Self-report use date',
                       'Which protocol did you use?': 'Mosq Protocol Used',
                       'Was this a training session?': 'Training sesh?',
                       'Did you park the Mosquito in position #3 and put everything back into the drawer after you were finished?': 'Cleaned-up?',
                       'How long did you use the Mosquito? (1 hr and 15 min → 1.25)': 'Mosq Dur (hr)'}, inplace=True)

    null_row = [
        [start_date, 'Stroud', 'Nobody', start_date, 'I used my own', 'TTP Standard 2µL (hanging drop)', '', 0, 'nan',
         'nan', 'nan', '', '', '', '', '', 0, 0, 0, '', '', '', '', '']]
    df = df.append(pd.DataFrame(null_row, columns=df.columns))

    # Look at 'Timestamp' column and convert to datetime type
    df.index = pd.to_datetime(df.pop('Timestamp'))
    df = df[df.index.notnull()]
    mask = (df.index >= start_date) & (df.index <= end_date)
    df = df.loc[mask]
    df['Group'] = df['Group'].map(lambda s: s.lower())  # make group name lowercase to standardize
    df['Mosq Tips'] = pd.to_numeric(df['Mosq Tips'], errors='coerce').fillna(0)  # convert objects to numeric
    df['NumSDP'] = pd.to_numeric(df['NumSDP'], errors='coerce').fillna(0)  # convert objects to numeric
    df['NumHDP'] = pd.to_numeric(df['NumHDP'], errors='coerce').fillna(0)  # convert objects to numeric
    df['Mosq Dur (hr)'] = pd.to_numeric(df['Mosq Dur (hr)'], errors='coerce').fillna(0)  # convert objects to numeric
    return df


def clean_DF_MosquitoLCP(df, dates):
    start_date, end_date = dates
    # Rename columns to make easier to read, NEED TO CHANGE IF CHANGES MADE IN GOOGLE FORM
    df.rename(columns={'How many tips did you use in total?': 'Mosq Tips',
                       'How many LCP plates did you set up?': 'Mosq LCP Plates Set-up',
                       'How many sitting drop plates did you set up? (Enter 0 if none)': 'NumSDP',
                       'How many hanging drop plates did you set up? (Enter 0 if none)': 'NumHDP',
                       'What is your name?': 'Name',
                       'Which lab are you from?': 'Group',
                       'What day did you use the Mosquito LCP?': 'Self-report use date',
                       'Which protocol did you use?': 'Mosq Protocol Used',
                       'Was this a training session?': 'Training sesh?',
                       'Did you park the Mosquito in position #3 and put everything back into the drawer after you were finished?': 'Cleaned-up?',
                       'How long did you use the Mosquito LCP? (1 hr and 15 min → 1.25)': 'Mosq Dur (hr)'},
              inplace=True)

    null_row = [
        [start_date, 'nan', 'nan', start_date, 'nan', 'nan', 0, 0, 'nan', 'nan', '', '', '', '', 0,
         'nan', '', '', '', '', '']]
    df = df.append(pd.DataFrame(null_row, columns=df.columns))

    df.index = pd.to_datetime(df.pop('Timestamp'))
    df = df[df.index.notnull()]
    mask = (df.index >= start_date) & (df.index <= end_date)
    df = df.loc[mask]
    df['Group'] = df['Group'].map(lambda s: s.lower())  # make group name lowercase to standardize
    # convert columns to numeric values as they should be
    df['Mosq LCP Plates Set-up'] = pd.to_numeric(df['Mosq LCP Plates Set-up'], errors='coerce')
    df['NumSDP'] = pd.to_numeric(df['NumSDP'], errors='coerce').fillna(0)
    df['NumHDP'] = pd.to_numeric(df['NumHDP'], errors='coerce').fillna(0)
    a = pd.to_numeric(df['Mosq Tips'].iloc[:, 0], errors='coerce').fillna(0)
    b = pd.to_numeric(df['Mosq Tips'].iloc[:, 1], errors='coerce').fillna(0)
    df['Cum Mosq Tips'] = a.add(b)
    return df



def clean_DF_Dragonfly(df, dates):
    start_date, end_date = dates

    df.rename(columns={
        'What lab are you from?': 'Group',
        'What is your name?': 'Name',
        'How many NEW tips/plungers did you use?': 'DFly New Tips',
        'How many NEW reservoirs did you use?': 'DFly New Reservoirs',
        'How many NEW MXOne tip arrays did you use?': 'DFly New Mixers',
        'What kind of plates did you use?': 'DFly Plate Type',
        'How many NEW plates did you use?': 'DFly New Plates',
        # 'How many screens did you set up?' ,: 'DFly New Plates Set-up'
    }, inplace=True)
    df.index = pd.to_datetime(df.pop('Timestamp'))
    df = df[df.index.notnull()]
    mask = (df.index >= start_date) & (df.index <= end_date)
    df = df.loc[mask]
    df['Group'] = df['Group'].map(lambda s: s.lower())  # make group name lowercase to standardize
    df['DFly New Tips'] = pd.to_numeric(df['DFly New Tips'], errors='coerce').fillna(0)  # convert objects to numeric
    df['DFly New Reservoirs'] = pd.to_numeric(df['DFly New Reservoirs'], errors='coerce').fillna(
        0)  # convert objects to numeric
    df['DFly New Mixers'] = pd.to_numeric(df['DFly New Mixers'], errors='coerce').fillna(
        0)  # convert objects to numeric
    df['DFly New Plates'] = pd.to_numeric(df['DFly New Plates'], errors='coerce').fillna(
        0)  # convert objects to numeric
    return df


def clean_DF_screenOrders(df, dates):
    start_date, end_date = dates
    df.rename(columns={
        'Lab': 'Group',
        'Name': 'Requested By',
        'SKU': 'Item Name',
        'Price': 'Unit Price',
        'Total price': 'Screens Total Cost',
    }, inplace=True)
    df = df.astype({"Screens Total Cost":"float64"})
    df.index = pd.to_datetime(df.pop('Date'))
    df = df[df.index.notnull()]
    mask = (df.index >= start_date) & (df.index <= end_date)
    # df = df.loc[start_date:end_date]
    df = df.loc[mask]

    df['Group'] = df['Group'].map(lambda s: s.lower())  # make group name lowercase to standardize
    return df
