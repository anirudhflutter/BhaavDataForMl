import pylab
import calendar
import numpy as np
import pandas as pd
from scipy import stats
#import missingno as msno
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
pd.options.mode.chained_assignment = None
warnings.filterwarnings("ignore", category=DeprecationWarning)
daily_Data= pd.read_csv("employee_file.csv")
print(daily_Data.head(2))
print(daily_Data.shape)
df=daily_Data.copy()
print(df.columns)
df=df.rename(index=str, columns={
    "Sl no.": "Sl_no", 
    "Min Price (Rs./Quintal)": "Min_Price",
    "Price Date":"Price_Date",
    "Modal Price (Rs./Quintal)":"Modal_Price"
    })
print(df.head())
df.Price_Date = pd.to_datetime(df.Price_Date, errors='coerce')
print(df.head())
df=df.sort_values(by='Price_Date')
df.drop_duplicates('Price_Date', inplace = True)
print(df.head(20))
df.to_csv("employee_file_.csv", sep=',')