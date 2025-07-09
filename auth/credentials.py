#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import datetime
import plotly.express as px
import os
from py5paisa import FivePaisaClient



#--------------------------------------------------------------------
#LOGIN CREDENTIALS
#SECURE ENCRYPTION NEEDS TO BE ESTABLISHED FOR THIS
#--------------------------------------------------------------------

def auth():
    cred={
        "APP_NAME":"",
        "APP_SOURCE":"",
        "USER_ID":"",
        "PASSWORD":"",
        "USER_KEY":"",
        "ENCRYPTION_KEY":""
        }

    return cred