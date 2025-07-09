#---------------------------------------------------
#IMPORT LIBRARIES & DEPENDENCIES
#---------------------------------------------------
import pandas as pd
import datetime
import os
import time


#--------------------------------------------------------------------
#IMPORT ALL INTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
from auth.credentials import *
from auth.client_secret import *
from scripts.data_refresh.data_refresh import *
from scripts.feature_generation.feature_generate import *
from scripts.ml_model.xgb_model import *
from scripts.ml_model.xgb_model_tuned import *
from scripts.trade_engine.trade_engine import *

#---------------------------------------------------
#INTIALIZE TERMINAL SCREEN
#---------------------------------------------------
screen_on=1

while(screen_on):
	os.system('cls')
	print("--------------------------------------------")
	print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
	print("| WELCOME TO NANOEDGE")
	print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
	print("--------------------------------------------")
	print("What would you like to do?")
	print("1. Refresh training dataset")
	print("2. Check timestamp for last refreshed training data")
	print("3. Train ML model for ETF predictions")
	print("4. Run trading engine")
	print("--------------------------------------------")
	#print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
	#print("--------------------------------------------")
	choice = input("Please enter your choice:")
	
	if int(choice)==1:
		os.system('cls')
		print("✾ Executing selection " + str(choice))
		cred=auth()
		data_refresh()
		print("✾ Data Refresh Completed - Returning to Main screen in 5 seconds")
		time.sleep(5)
	elif int(choice)==2:
		os.system('cls')
		print("✾ Executing selection " + str(choice))
		print("Current Training Data starts from "+str(start_date)+" extending up to "+str(end_date))
		print("✾ Returning to Main screen in 5 seconds")
		time.sleep(5)
	elif int(choice)==3:
		os.system('cls')
		print("✾ Executing selection " + str(choice))
		print("Creating features for training ML model")
		feature_generate()		
		xgb_model_train_tune()
		#exit()
		print("✾ Returning to Main screen in 5 seconds")
		time.sleep(5)
	elif int(choice)==4:
		os.system('cls')
		print("✾ Executing selection " + str(choice))
		trade_engine()
		os.system('cls')
		print("✾ Returning to Main screen in 5 seconds")

	else:
		os.system('cls')
		print("✾ Invalid selection - Exiting Program")
		#print(screen_on)
		screen_on=0
		#print(screen_on)
		#exit()