#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import datetime
import os
import sys
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics



def xgb_model_train():
	#--------------------------------------------------------------------
	#SECTION 0 - INTERNAL VARIABLE DECLARATION
	#--------------------------------------------------------------------
	save_path='data/features'
	scrip_name=['ASIANPAINT','EICHERMOT','HEROMOTOCO','TATAMOTORS','APOLLOHOSP','SBIN','M&M',
          'BEL','JSWSTEEL','ICICIBANK','INDUSINDBK','ONGC','BAJAJ-AUTO','BRITANNIA','NESTLEIND',
          'HINDALCO','RELIANCE','TRENT','TATASTEEL','DRREDDY','SHRIRAMFIN','KOTAKBANK','HDFCBANK',
          'AXISBANK','NTPC','TECHM','SBILIFE','CIPLA','GRASIM','HINDUNILVR','LT','TATACONSUM','WIPRO',
          'TITAN','BPCL','INFY','SUNPHARMA','TCS','MARUTI','HCLTECH','COALINDIA','ULTRACEMCO','GOLDIETF']

	#target_name=['NIFTY','SETFNIF50']
	target_name=['SETFNIF50']

	
	#--------------------------------------------------------------------
	#SECTION 1 - READ FEATURE SET FOR TRAINING
	#--------------------------------------------------------------------
	df=pd.read_csv(save_path+"/"+"feature.csv")
	#print(df)
	train=df[scrip_name]
	target=df[target_name]
	#print(train)
	#print(target)
	
	X=train.copy()
	Y=target.copy()

	#--------------------------------------------------------------------
	#SECTION 2 - TRAIN XGBOOST MODEL
	#--------------------------------------------------------------------
	#print(X)
	#print(Y)
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
	#print(X.shape, X_train.shape, X_test.shape)
	regressor = XGBRegressor()
	regressor.fit(X_train, Y_train)

	

	#--------------------------------------------------------------------
	#SECTION 3 - CHECK ERROR RATES FOR MODEL
	#--------------------------------------------------------------------
	data_prediction = regressor.predict(X_test)
	#print(X_test)
	#print(data_prediction)
	predicted_df=X_test.copy()
	predicted_df['ETF_Predicted']=data_prediction
	predicted_df['ETF_actual']=Y_test
	r2_data = metrics.r2_score(Y_test, data_prediction)
	return r2_data
	#print('R Squared value for standard model = ', r2_data)
	#print(predicted_df)
	#exit()