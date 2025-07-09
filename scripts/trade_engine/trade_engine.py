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
import plotext as plt
	
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

def trade_engine():

	
	
	#-----------------------------------------------------------------------------------------
	#SET UP GLOBAL PARAMETERS
	#WHENEVER RETRAINING MODEL - ALWAY CHECK IF SCRIP_NAME LIST MATCHES WITH TRAINING DATASET
	#-----------------------------------------------------------------------------------------
	equitycode="10176"
	equityname="SETFNIF50"
	positional_value=0
	positional_qty=0
	pos_size=5
	sell_threshold=1.05
	pred_etf_vector=[]
	actual_etf_vector=[]
	
	scrip_name=['ASIANPAINT', 'EICHERMOT', 'HEROMOTOCO', 'TATAMOTORS', 'APOLLOHOSP',
	       'SBIN', 'M&M', 'BEL', 'JSWSTEEL', 'ICICIBANK', 'INDUSINDBK', 'ONGC',
	       'BAJAJ-AUTO', 'BRITANNIA', 'NESTLEIND', 'HINDALCO', 'RELIANCE', 'TRENT',
	       'TATASTEEL', 'DRREDDY', 'SHRIRAMFIN', 'KOTAKBANK', 'HDFCBANK',
	       'AXISBANK', 'NTPC', 'TECHM', 'SBILIFE', 'CIPLA', 'GRASIM', 'HINDUNILVR',
	       'LT', 'TATACONSUM', 'WIPRO', 'TITAN', 'BPCL', 'INFY', 'SUNPHARMA',
	       'TCS', 'MARUTI', 'HCLTECH', 'COALINDIA', 'ULTRACEMCO', 'GOLDIETF']


	scrip_code=['236','910','1348','3456','157','3045','2031','383','11723',
	'4963','5258','2475','16669','547','17963','1363','2885','1964','3499',
	'881','4306','1922','1333','5900','11630','13538','21808','694','1232','1394',
	'11483','3432','3787','3506','526','1594','3351','11536','10999','7229','20374','11532','19679']
	delta_vector=[]
	
	def get_curr_time_1():
		current_datetime = dd.now()
		current_time = current_datetime.time()
		curr_time_string=str(current_time)
		return curr_time_string
	
	
	init_data = {
	    'Date': [str(datetime.datetime.today()).split()[0]],
	    'Time': [get_curr_time_1()],
	    'Transaction_Type': ['NA'],
	    'Qty': [0],
	    'Price': [0],
	    'Value': [0]
	}
	
	trade_log = pd.DataFrame(init_data)
	#print(trade_log)
	
	
	
	cred=auth()
	client = FivePaisaClient(cred=cred)
	client.get_totp_session(client_secret(),input("Enter TOTP for Authentication >>> "),dob())
	
	
	def sell_trigger(client,positional_value,positional_qty,equityname):
		print("Checking Opportunity to Sell")
		if(positional_qty>0):


			a=[{"Exchange":"N","ExchangeType":"C","ScripCode":equitycode}]
			etf_info=client.fetch_market_snapshot(a)
			etf_info_df = pd.DataFrame(etf_info)
			etf_price=(etf_info_df['Data'].iloc[0])
			etf_price=etf_price['LastTradedPrice']
			etf_price=float(etf_price)
			#etf_info=client.query_scrips("N","C",equityname,"0","XX","")
			#print(etf_info)
			#etf_price=float(etf_info['StrikeRate'].iloc[0])
			#etf_price=random.randint(255, 280)
			notional_value=etf_price*positional_qty
			print("Current Notional Value is :"+str(notional_value))
			if (notional_value>sell_threshold*positional_value):
				print("Liquidating Entire Position")
				log_info=[str(datetime.datetime.today()).split()[0],get_curr_time_1(),'Sell',positional_qty,etf_price,positional_qty*etf_price]
				trade_log.loc[len(trade_log)] = log_info
				#DO NOT UNCOMMENT BELOW CODE
				#client.squareoff_all()
				return 0
			else:
				print("No Liquidation initiated")
				return positional_value
		else:
			print("No Liquidation initiated")
			return positional_value
	
	
	
	
	def check_mkt_time():
		current_datetime = dd.now()
		current_time = current_datetime.time()
		curr_time_string=str(current_time)
		hour=int(curr_time_string[:2])
		valid_hour_list=[9,10,11,12,13,14]
		#print(hour)
		#print(current_time)
		if(hour in valid_hour_list):
			mkt_open=1
		else:
			mkt_open=0
			print("Market is currently closed. Please come back later!")
		return mkt_open
	
	#print(mkt_open)
	#exit()
	
	mkt_open=check_mkt_time()
	
	retraining_data=pd.DataFrame(columns=scrip_name)
	
	
	#exit()
	
	#mkt_open=5
	#feature_vector_ctr=0
	while(mkt_open):
		os.system('cls')
		print("[-------------------------------------------------------------]")
		print("[------------Running Trade Engine (NanoEdge)------------------]")
		print("[-------------------------------------------------------------]")
	
		print("\n")
		print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
		print("|⇒⇒⇒⇒Checking Liquidation Opportunity⇒⇒⇒⇒")
		print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
	
	
		if (positional_value==0):
			positional_qty=0
		
		print("Current Positional Value is "+str(positional_value))
		print("Current Positional Quantity is "+str(positional_qty))
		positional_value=sell_trigger(client,positional_value,positional_qty,equityname)
		time.sleep(5)


		feature_vector = pd.DataFrame([str(datetime.datetime.today()).split()[0]], columns=['Date'])
		#print(feature_vector)
		
		i=0
		for name in scrip_code:
			print("Preparing Real Time Feature Vector for running ML prediuction")
			#scrip_info=client.query_scrips("N","C",name,"0","XX","")
			a=[{"Exchange":"N","ExchangeType":"C","ScripCode":name}]
			scrip_info=client.fetch_market_snapshot(a)
			#print(scrip_info)
			scrip_info_df = pd.DataFrame(scrip_info)
			scrip_price=(scrip_info_df['Data'].iloc[0])
			scrip_price=scrip_price['LastTradedPrice']
			scrip_price=float(scrip_price)
			#print(scrip_info)
			#price=float(scrip_info['StrikeRate'].iloc[0])
			#price=random.randint(100, 3000)
			price=scrip_price
			feature_vector[scrip_name[i]]=price
			i=i+1
			os.system('cls')

		
		
		#feature_vector_ctr=feature_vector_ctr+1
		pred_vector=feature_vector[scrip_name].copy()
		print("The Feature Vector is:")
		print(pred_vector)


		#--------------------------------------------------------
		#Concatenation with blank dataframe is deprecated
		#This code will have to be changed later on
		#--------------------------------------------------------
		todays_save_date=str(datetime.datetime.today()).split()[0]
		retraining_data=pd.concat([retraining_data, pred_vector])
		save_path_retraining='data/retraining_data'
		retraining_data.to_csv(save_path_retraining+"/"+"feature_vector_"+todays_save_date+".csv")

		
		#print(pred_vector)
		
		# Load the saved model
		loaded_model = xgb.XGBRegressor()
		loaded_model.load_model('data/model/xgboost_model.json')
		etf_pred = loaded_model.predict(pred_vector)
		#print(etf_pred)
		
		
		
		
		
		a=[{"Exchange":"N","ExchangeType":"C","ScripCode":equitycode}]
		etf_info=client.fetch_market_snapshot(a)
		etf_info_df = pd.DataFrame(etf_info)
		etf_price=(etf_info_df['Data'].iloc[0])
		etf_price=etf_price['LastTradedPrice']
		etf_price=float(etf_price)

		#etf_info=client.query_scrips("N","C",equityname,"0","XX","")
		#print(etf_info)
		#etf_price=float(etf_info['StrikeRate'].iloc[0])
		#etf_price=random.randint(230, 255)
		
	
	
		print("\n")
		print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
		print("|⇒⇒⇒⇒Checking Purchase Opportunity⇒⇒⇒⇒⇒⇒")
		print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
	
		print("Predicted price for ETF is "+str(float(etf_pred[0])))
		print("Market price for ETF is "+str(etf_price))
	
		pred_value=float(etf_pred[0])
		actual_value=float(etf_price)
		delta=pred_value-actual_value
		print("Delta is "+str(delta))
	
	
		pred_etf_vector.append(pred_value)
		actual_etf_vector.append(actual_value)
	
		#y=plt.sin()
		#print(y)
	
		print("Printing Predicted & Actual Price Vectors")
		print(pred_etf_vector)
		print(actual_etf_vector)
	
		#plt.cld()
		#plt.scatter(pred_etf_vector, label='Predicted ETF Price')
		#plt.scatter(actual_etf_vector,label='Actual ETF Price')
		#plt.plotsize(80, 20)
		#plt.xlim(1, 200)
		#plt.ylim(230,270)
		##plt.grid(1,10)
		##plt.scatter(actual_etf_vector, label = "Actual ETF Price")
		#plt.title("ETF Price")
		#plt.show()
		
		print("\n")
		print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
		print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒Execution Log⇒⇒⇒⇒⇒⇒⇒⇒⇒")
		print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
		
		if delta>0:
			delta_vector.append(delta)
	
		print("Delta Vector - Current Status: " + str(delta_vector))
		delta_vector_length=len(delta_vector)
		print("Delta Vector Length is " + str(delta_vector_length))
	
	
	
		#make sure to incorporate brokerage value and taxes into positional value
		if delta_vector_length==30 or delta_vector_length==60 or delta_vector_length==10:
			print("Executing ETF buy transaction")
			#DO NOT UNCOMMENT BELOW CODE
			#client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = int(equitycode), Qty=int(pos_size), Price=0)
			log_info=[str(datetime.datetime.today()).split()[0],get_curr_time_1(),'Buy',pos_size,actual_value,pos_size*actual_value]
			trade_log.loc[len(trade_log)] = log_info
			positional_value=positional_value+((actual_value*pos_size)+20)+(0.00025*actual_value*pos_size)
			positional_qty=positional_qty+pos_size
		else:
			print("Delta Vector doesnt meet threshold - Cant execute Buy Transaction")
	
		
		print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
		print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
	
		save_path='data/execution_log'
		trade_log.to_csv(save_path+"/"+"trade_log.csv")
		#mkt_open=mkt_open-1
		mkt_open=check_mkt_time()
	
		pred_matrix={'predicted_value':pred_etf_vector,'actual_value':actual_etf_vector}
		prediction_log = pd.DataFrame(pred_matrix)
		#print(prediction_log)
		prediction_log.to_csv(save_path+"/"+"prediction_log.csv")
		time.sleep(5)
		os.system('cls')
		
