#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import os
import sys



#--------------------------------------------------------------------
#RESET EXECUTION PATH TO MAIN FOLDER
#--------------------------------------------------------------------
#os.chdir("..")
#os.chdir("..")
#current_directory=os.getcwd()
#sys.path.append(current_directory)

#--------------------------------------------------------------------
#IMPORT ALL INTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
from auth.credentials import *
from auth.client_secret import *


#--------------------------------------------------------------------
#SECTION 0 - INTERNAL VARIABLE DECLARATION
#THE SCRIP NAME VARIABLE HAS NO USAGE FOR THIS SCRIPT AND IS REDUNDANT
#--------------------------------------------------------------------
scrip_name=['ASIANPAINT','EICHERMOT','HEROMOTOCO','TATAMOTORS','APOLLOHOSP','SBIN','M&M',
          'BEL','JSWSTEEL','ICICIBANK','INDUSINDBK','ONGC','BAJAJ-AUTO','BRITANNIA','NESTLEIND',
          'HINDALCO','RELIANCE','TRENT','TATASTEEL','DRREDDY','SHRIRAMFIN','KOTAKBANK','HDFCBANK',
          'AXISBANK','NTPC','TECHM','SBILIFE','CIPLA','GRASIM','HINDUNILVR','LT','TATACONSUM','WIPRO',
          'TITAN','BPCL','INFY','SUNPHARMA','TCS','MARUTI','HCLTECH','COALINDIA','ULTRACEMCO','NIFTY','GOLDIETF','SETFNIF50']


start_date='2021-01-01'
#end_date=str(datetime.datetime.today()).split()[0]
end_date='2025-07-08'
#format-YYYY-MM-DD    

#--------------------------------------------------------------------
#LOGIN CREDENTIALS
#SECURE ENCRYPTION NEEDS TO BE ESTABLISHED FOR THIS
#--------------------------------------------------------------------
cred=auth()



def data_refresh():   

    #--------------------------------------------------------------------
    #PREPARE MASTER DATA
    #--------------------------------------------------------------------

    nifty_master_path='data/masterdata/nifty_master.csv'
    nifty_master = pd.read_csv(nifty_master_path)
    
    ScripCode = nifty_master['ScripCode'].values.tolist()
    ScripName = nifty_master['Name'].values.tolist()
    
    client = FivePaisaClient(cred=cred)
    client.get_totp_session(client_secret(),input("Enter TOTP for Authentication >>> "),dob())
    
    new_path='data/tickdata'
    os.chdir(new_path)
    
    i=0
    for code in ScripCode:
        #print(code)
        df=client.historical_data('N','C',code,'1d',start_date,end_date)
        df['ScripName']=ScripName[i]
        df['ScripCode']=code
        file_name=str(code)+'.csv'
        print("Saving Data Frame for Scrip "+file_name)
        df.to_csv(file_name)
        i=i+1
