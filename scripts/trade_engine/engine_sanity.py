#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import numpy as np
import datetime
import os
import sys
from xgboost import XGBRegressor
import xgboost as xgb
import time
from datetime import datetime as dd
import random

#--------------------------------------------------------------------
#RESET EXECUTION PATH TO MAIN FOLDER
#--------------------------------------------------------------------
os.chdir("..")
os.chdir("..")
current_directory=os.getcwd()
sys.path.append(current_directory)



#--------------------------------------------------------------------
#IMPORT ALL INTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
from auth.credentials import *
from auth.client_secret import *

equitycode="10176"
equityname="SETFNIF50"
pos_size=5

cred=auth()
client = FivePaisaClient(cred=cred)
client.get_totp_session(client_secret(),input("Enter TOTP for Authentication >>> "),dob())


#etf_info=client.query_scrips("N","C",equityname,"0","XX","")
#print(etf_info)
#etf_info_df = pd.DataFrame(etf_info)
#etf_info_df.to_csv("engine_sanity_log.csv")



#etf_price=float(etf_info['StrikeRate'].iloc[0])
#print(etf_price)

#client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = int(equitycode), Qty=int(pos_size), Price=0)

#req_list=[
#            { "Exch":"N","ExchType":"C","ScripCode":10176},
#            ]
#
#req_data=client.Request_Feed('mf','s',req_list)
#def on_message(ws, message):
#    print(message)
#
#
#client.connect(req_data)
#
#etf_info=client.receive_data(on_message)
#
#etf_info_df = pd.DataFrame(etf_info)
#etf_info_df.to_csv("engine_sanity_log.csv")
#
#etf_price=float(etf_info_df['LastQty'].iloc[0])
#print(etf_price)




#------------------------------------------------------------
#Working Code to get live Market Data
#------------------------------------------------------------
a=[{"Exchange":"N","ExchangeType":"C","ScripCode":"10176"}]
#print(client.fetch_market_snapshot(a))

etf_info=client.fetch_market_snapshot(a)

etf_info_df = pd.DataFrame(etf_info)
etf_info_df.to_csv("engine_sanity_log.csv")

etf_price=(etf_info_df['Data'].iloc[0])
print(etf_price)
etf_price=etf_price['AverageTradePrice']

print("Printing ETF Price")
print(etf_price)
#------------------------------------------------------------
#End of Working Code
#------------------------------------------------------------


#start_date='2025-01-01'
#end_date='2025-07-06'
#df=client.historical_data('N','C',equitycode,'60m',start_date,end_date)
#print(df)
