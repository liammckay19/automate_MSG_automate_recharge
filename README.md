# automate_MSG_automate_recharge


 Automates Loren Jiang's scripts and Google Sheets for doing 1 month previous. If today was January 12, 2020 it would download google forms and calculate recharge for December 1, 2019 to January 1, 2019 
 
 GUI automation in the RockImager software has been added and scheduled to download data for the last month. It automatically uploads these files to Google Drive <code> ljiang > xrayFacilityRecharge > equipmentLogs > RockImagerEventLogs > rockImager[20c,4c]</code>
 
 With the addition of a scheduled GUI automation to the RockImagers in the 4C and 20C room, taking time out of downloading Drive files will add time to the lab manager's day.

## Installation

Clone this repo: 

1. <code>git clone https://github.com/liammckay19/automate_MSG_automate_recharge</code>

2. <code> python3 -m venv recharge_auto_env </code> --important for automation to have the same environment name

3. <code>pip install -r requirements.txt</code>

4. <code> deactivate </code>

5. activate automate_msg_automate_recharge environment <code> source recharge_auto_env/bin/activate </code>

6. Put "mycreds" file in the same directory

## Usage
### 1. Upload GL and DPE from last month to the Google Spreadsheet

Upload Excel spreadsheets to My Drive > ljiang > xrayFacilityRecharge > GL_DPE > excelOriginals and rename with format [month]_[year] [GL/DPE] File name and location are important various scripts.

- In the GL_DPE folder, open the Google sheet collatedGL_DPE and under Custom functions run Make copies from Excel. This will create Google sheet copies in the sheetsCopies folder.
- Run the custom function Collate itemized recharge. 

If there is an error at this step, it will mostly be due to how certain column headers are named. You might need to rename certain columns to match the format of existing Google sheets.

Note, although not recommended, you can also directly enter the GL and DPE data into collatedGL_DPE Google sheet, but be sure to format cell values accordingly.

### 2. Run automation (the reason to use this script)

- Activate automate_msg_automate_recharge environment <code> source recharge_auto_env/bin/activate </code>
- <code>python createRecharge.py</code>

#### What does createRecharge.py do? (things you don't have to do)
- download from google drive the 20c and 4c logs
- calculate recharge for the last month from today (if today is 1/20/2020, it will calculate from 12/1/2019 to 1/1/2020)
- upload rechargeSummaryYYYY_MM_DD_TO_YYYY_MM_DD.xlsx to google drive <code> xrayFacilityRecharge > monthlyRecharge </code>

## Known Errors
- going from 12/1/2020 to 1/1/2021 will not be named correctly in the RockImager Google Drive. It will be 12/1/2020_TO_1/1/2020
