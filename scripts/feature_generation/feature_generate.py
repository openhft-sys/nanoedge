#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import datetime
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
#SECTION 0 - INTERNAL VARIABLE DECLARATION
#--------------------------------------------------------------------
scrip_name=['ASIANPAINT','EICHERMOT','HEROMOTOCO','TATAMOTORS','APOLLOHOSP','SBIN','M&M',
          'BEL','JSWSTEEL','ICICIBANK','INDUSINDBK','ONGC','BAJAJ-AUTO','BRITANNIA','NESTLEIND',
          'HINDALCO','RELIANCE','TRENT','TATASTEEL','DRREDDY','SHRIRAMFIN','KOTAKBANK','HDFCBANK',
          'AXISBANK','NTPC','TECHM','SBILIFE','CIPLA','GRASIM','HINDUNILVR','LT','TATACONSUM','WIPRO',
          'TITAN','BPCL','INFY','SUNPHARMA','TCS','MARUTI','HCLTECH','COALINDIA','ULTRACEMCO','NIFTY','GOLDIETF','SETFNIF50']

#start_date='2025-01-01'


def feature_generate():
    #--------------------------------------------------------------------
    #SET-UP ALL PATH VARIABLES
    #--------------------------------------------------------------------
    nifty_master_path='data/masterdata/nifty_master.csv'
    temp_path='data/tickdata'
    new_path='data/tickdata'
    save_path='data/features'
    
    #--------------------------------------------------------------------
    #READ MASTER FILE TO GET ALL SCRIP NAMES
    #--------------------------------------------------------------------
    nifty_master = pd.read_csv(nifty_master_path)
    ScripCode = nifty_master['ScripCode'].values.tolist()
    ScripName = nifty_master['Name'].values.tolist()
    
    #--------------------------------------------------------------------
    #READ SCRIP WISE DAILY MARKET DATA
    #--------------------------------------------------------------------	
    new_path=new_path+'/'+str(ScripCode[0])+'.csv'
    market_data = pd.read_csv(new_path)
    #market_data['daily_return']=(market_data['Close']-market_data['Open'])/market_data['Open']
    
    for code in ScripCode:
    	new_path=temp_path
    	new_path=new_path+'/'+str(code)+'.csv'
    	additional_market_data=pd.read_csv(new_path)
    	market_data=pd.concat([market_data, additional_market_data])
    	
    market_data=market_data.drop_duplicates()
    market_data.dropna(inplace=True)
    
    market_data_pivot = pd.pivot_table(market_data,
                                     values='Close',  # Column to aggregate
                                     index='Datetime',  # Column(s) for rows
                                     columns='ScripName',  # Column(s) for columns
                                     aggfunc='mean')
    
    market_data_pivot.dropna(inplace=True)
    market_data_pivot.to_csv(save_path+"/"+"feature.csv")
    #print(market_data_pivot['NIFTY'])
