#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import numpy as np
import datetime
import os
import sys
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics
import xgboost as xgb
from sklearn.metrics import accuracy_score
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from sklearn.metrics import mean_squared_error
from sklearn.metrics import root_mean_squared_error
from hyperopt.pyll.base import scope
import time


#--------------------------------------------------------------------
#IMPORT ALL INTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
from scripts.ml_model.xgb_model import *

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
#print(train.columns)
#print(target)

X=train.copy()
Y=target.copy()

X.to_csv("train.csv")
#exit()


#--------------------------------------------------------------------
#SECTION 2 - TRAIN XGBOOST MODEL
#--------------------------------------------------------------------
print(X)
print(Y)
#X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
#X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 0)
X_train, X_valid, y_train, y_valid = train_test_split(X, Y, random_state=3, train_size=.8)
#print(X.shape, X_train.shape, X_test.shape)
#X_train.to_csv("train.csv")
#exit()


#Define the hyperopt objective.
def hyperparameter_tuning(space):
    
    model = xgb.XGBRegressor(**space,eval_metric="rmse",early_stopping_rounds=100)
    
    #Define evaluation datasets.
    evaluation = [(X_train, y_train), (X_valid, y_valid)]
    
    #Fit the model. Define evaluation sets, early_stopping_rounds, and eval_metric.
    model.fit(X_train, y_train,
            eval_set=evaluation
            ,verbose=False)

    #Obtain prediction and rmse score.
    pred = model.predict(X_valid)
    rmse = mean_squared_error(y_valid, pred, squared=False)
    print ("SCORE:", rmse)
    
    #Specify what the loss is for each model.
    os.system('cls')
    return {'loss':rmse, 'status': STATUS_OK, 'model': model}



def xgb_model_train_tune():

	
	#Define the space over which hyperopt will search for optimal hyperparameters.
	space = {'max_depth': scope.int(hp.quniform("max_depth", 1, 5, 1)),
        'gamma': hp.uniform ('gamma', 0,1),
        'reg_alpha' : hp.uniform('reg_alpha', 0,50),
        'reg_lambda' : hp.uniform('reg_lambda', 10,100),
        'colsample_bytree' : hp.uniform('colsample_bytree', 0,1),
        'min_child_weight' : hp.uniform('min_child_weight', 0, 5),
        'n_estimators': 10000,
        'learning_rate': hp.uniform('learning_rate', 0, .3),
        'random_state': 5,
        'max_bin' : scope.int(hp.quniform('max_bin', 200, 550, 1))}





	
	

	

	trials = Trials()
	best = fmin(fn=hyperparameter_tuning,
	            space=space,
	            algo=tpe.suggest,
	            max_evals=30,
	            trials=trials)
	

	os.system('cls')

	print("The best hyperparameters are : ")
	print("---------------------------------------------")
	print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
	print("")
	print(best)
	print("")
	print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
	print("---------------------------------------------")

	time.sleep(2)
	os.system('cls')

	print("Model Comparision (Tuned vs Base) : ")
	print("---------------------------------------------")
	print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")	
	#Create instace of best model.
	best_model = trials.results[np.argmin([r['loss'] for r in 
    trials.results])]['model']

	xgb_preds_best = best_model.predict(X_valid)
	xgb_score_best = root_mean_squared_error(y_valid, xgb_preds_best)
	print('RMSE_Best_Model:', xgb_score_best)

	xgb_standard = xgb.XGBRegressor().fit(X_train, y_train)
	standard_score = root_mean_squared_error(y_valid, xgb_standard.predict(X_valid))
	print('RMSE_Standard_Model:', standard_score)
	print("---------------------------------------------")
	print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")

	time.sleep(5)	
	os.system('cls')

	#--------------------------------------------------------------------
	#SECTION 3 - CHECK ERROR RATES FOR MODEL
	#--------------------------------------------------------------------
	#data_prediction = regressor.predict(X_test)
	data_prediction = best_model.predict(X_valid)
	#print(X_valid)
	#print(data_prediction)
	predicted_df=X_valid.copy()
	predicted_df['ETF_Predicted']=data_prediction
	predicted_df['ETF_actual']=y_valid
	r2_data = metrics.r2_score(y_valid, data_prediction)
	print('R Squared value for Trained Model = ', r2_data)
	r2_data_standard=xgb_model_train()
	print('R Squared value for Standard model = ', r2_data_standard)
	time.sleep(3)	
	os.system('cls')
	


	print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")
	print("Saving Model for future use by Trade Engine")
	print("|⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒⇒")

	time.sleep(2)
	os.system('cls')
	best_model.save_model('data/model/xgboost_model.json')
	#print(predicted_df)
	#exit()