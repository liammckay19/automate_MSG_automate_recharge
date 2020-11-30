#!usr/bin/bash
source ~/Documents/automate_MSG_automate_recharge/recharge_auto_env/bin/activate
if [ ! -d "~/Documents/automate_MSG_automate_recharge/rockimagerBacklogs/" ]
then 
	mkdir ~/Documents/automate_MSG_automate_recharge/rockimagerBacklogs
fi

mkdir ~/Documents/automate_MSG_automate_recharge/temp

echo "downloading rockimager log files"
python ~/Documents/automate_MSG_automate_recharge/downloadRockimagerFiles.py


echo 'calculating recharge'
python ~/Documents/automate_MSG_automate_recharge/calculateRecharge_auto.py ~/Documents/automate_MSG_automate_recharge/temp/20c* ~/Documents/automate_MSG_automate_recharge/temp/4c*


mv ~/Documents/automate_MSG_automate_recharge/temp/*.txt ~/Documents/automate_MSG_automate_recharge/rockimagerBacklogs/


echo "uploading to google drive"
python ~/Documents/automate_MSG_automate_recharge/uploadGDriveMonthlyRecharges.py
deactivate