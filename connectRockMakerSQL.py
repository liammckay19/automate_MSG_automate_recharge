import pyodbc 
import pandas as pd

SQL_DRIVER = '/usr/local/lib/libmsodbcsql.17.dylib'
rockmaker_conn = pyodbc.connect('Driver='+SQL_DRIVER+';'
                      'Server=//RI1000-0215;'
                      'Database=RockMaker;'
                      'UID=Formulatrix'
                      'PWD=i64tbtwl'
                      'Trusted_Connection=yes;')

rockimager_conn = pyodbc.connect('Driver='+SQL_DRIVER+';'
                      'Server=//RI1000-0215;'
                      'Database=RockMaker;'
                      'UID=Formulatrix'
                      'PWD=i64tbtwl'
                      'Trusted_Connection=yes;')

cursor = rockmaker_conn.cursor()

groups_df = pd.read_sql_query('SELECT ID,Name FROM RockMaker.dbo.Groups',rockmaker_conn)
groups_df['GroupID'] = groups_df["ID"]
groups_df = groups_df[groups_df.GroupID>=3]
groupUser_df = pd.read_sql_query('SELECT ID,GroupID,UserID FROM RockMaker.dbo.GroupUser',rockmaker_conn)

user_df = pd.read_sql_query('SELECT ID,Name,EmailAddress FROM RockMaker.dbo.Users',rockmaker_conn)
user_df['UserID'] = user_df["ID"]

group_id_user_id_df = pd.merge(user_df, groupUser_df, how='inner', on='UserID')

all_rockmaker_users_df = pd.merge(group_id_user_id_df, groups_df, how='inner', on='GroupID')

all_rockmaker_users_df = all_rockmaker_users_df.rename(columns={'Name_x':'RockMakerUsername', 'Name_y':'Group'})

print(all_rockmaker_users_df[['RockMakerUsername','EmailAddress','Group']])


# GET PLATE TO USER
plate_df = pd.read_sql_query('SELECT ID,Barcode,ExperimentID FROM RockMaker.dbo.Plate',rockmaker_conn)
plate_df = plate_df.rename(columns={'Barcode':'PlateBarcode', 'ID':'PlateID'})

experiment_df = pd.read_sql_query('SELECT ID,UserID FROM RockMaker.dbo.Experiment',rockmaker_conn)
experiment_df = experiment_df.rename(columns={'ID':'ExperimentID'})

# join on experimentid
plate_experiment_barcode_df = pd.merge(plate_df,experiment_df,how='inner',on='ExperimentID')

plate_experiment_barcode_name_group = pd.merge(
	plate_experiment_barcode_df,
	user_df,
	how='inner',
	on='UserID')

# GET IMAGING LOG
imagingLog_df = pd.read_sql_query('SELECT PlateBarcode,StartTime,EndTime,RobotID FROM RockImager.dbo.ImagingLog',rockimager_conn)

# TIE IMAGE LOG TO USER then to GROUP

imagingLog_user_df = pd.merge(imagingLog_df, plate_experiment_barcode_df, how='inner', on='PlateBarcode')

imagingLog_group_df = pd.merge(imagingLog_user_df, all_rockmaker_users_df, how='inner', on='UserID')


imagingLog_group_df["Duration"] = imagingLog_group_df['EndTime']-imagingLog_group_df['StartTime']
print(imagingLog_group_df)