import os
import subprocess
import csv
import pandas as pd

def get_orders_df_from_xtalscreenorder_pythonanywhere_website():
    # going to shop/order_csv and downloading to screen_orders.csv
    subprocess.run(['wget', 'https://xtalscreenorder.pythonanywhere.com/shop/order_csv', '--no-check-certificate', '-O', 'screen_orders.csv'])
    rows = []
    with open('screen_orders.csv', 'r') as f:
        for i,line in enumerate(f.readlines()):
            if i ==0:
                headers = line.rstrip().replace("\"","").replace("_"," ").split(",")
                headers.insert(0,' ')
                rows.append(headers[1:])
            else:
                rows.append(line.rstrip().replace("\"","").split(",")[1:])
    # print(rows[0])
    orders_df = pd.DataFrame(rows[1:], columns=rows[0])
    orders_df = orders_df.dropna()
    return orders_df

def main():
    get_orders_df_from_xtalscreenorder_pythonanywhere_website()

if __name__=="__main__":
    main()