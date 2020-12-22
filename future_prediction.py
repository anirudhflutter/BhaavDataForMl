import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import os
import glob
from csv import reader
import csv
import re
import GetPrice
import pymongo
import json
from matplotlib import pyplot
import seaborn as sns
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error, mean_absolute_error
plt.style.use('fivethirtyeight')

def trainingmodel(df,MandiFileName,cropname):
    array = df.values
    print("array")
    print(array)
    X = array[:, 0:1]
    Y = array[1:]
    print("Data of X")
    print(X)
    print("Data of Y")
    print(Y)
    print("Data of df")
    print(df)
    test_size = 0.33
    seed = 7
    # X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=test_size, random_state=seed)

    # df.Price_Date = pd.to_datetime(df.Price_Date, errors='coerce')
    df = df.set_index('Price_Date')
    print(df.head(2))

    data = df.copy()
    y = data

    # The 'MS' string groups the data in buckets by start of the month
    y = y['Modal_Price'].resample('MS').mean()

    # The term bfill means that we use the value before filling in missing values
    y = y.fillna(y.bfill())
    # y.plot(figsize=(15, 6))
    # plt.show()
    p = d = q = range(0, 2)

    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))

    # Generate all different combinations of seasonal p, q and q triplets
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    # print('Examples of parameter combinations for Seasonal ARIMA...')
    # print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
    # print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
    # print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
    # print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

    warnings.filterwarnings("ignore")  # specify to ignore warning messages

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()
                # results.save("finaldata.pkl")
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue

    # with open("finaldata.pkl", 'rb') as file:
    #     Pickled_LR_Model = pickle.load(file)
    # print("results are")
    # print(Pickled_LR_Model)

    pred_uc = results.get_forecast(steps=20)
    plt.style
    print("pred_uc")
    print(pred_uc)
    # Get confidence intervals of forecasts
    pred_ci = pred_uc.conf_int()



    print("predicted price for %s are" %MandiFileName)
    print(pred_ci)

    pred_ci.columns=["Lower Modal Price","Upper Model Price"]

    return pred_ci
    # pred_ci.to_csv("predicted_wheat_.csv")
    # results.plot_diagnostics(figsize=(15, 12))
    # plt.show()

    # pred = results.get_prediction(start=pd.to_datetime('2016-01-01'), dynamic=False)
    # pred_ci = pred.conf_int()
    #
    # ax = y['1990':].plot(label='observed')
    # pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)
    #
    # ax.fill_between(pred_ci.index,
    #                 pred_ci.iloc[:, 0],
    #                 pred_ci.iloc[:, 1], color='k', alpha=.2)
    #
    # ax.set_xlabel('Date')
    # ax.set_ylabel('Crop Price')
    # plt.legend()
    #
    # plt.show()
    #
    # y_forecasted = pred.predicted_mean
    # y_truth = y['2016-01-01':]
    #
    # # Compute the mean square error
    # mse = ((y_forecasted - y_truth) ** 2).mean()
    # print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

    # Get forecast 20 steps ahead in future

    # ax = y.plot(label='observed', figsize=(20, 15))
    # pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    # ax.fill_between(pred_ci.index,
    #                 pred_ci.iloc[:, 0],
    #                 pred_ci.iloc[:, 1], color='k', alpha=.25)
    # ax.set_xlabel('Date')
    # ax.set_ylabel('CROP PRICE')
    #
    # plt.legend()
    # plt.show()


# def trainingmodel(df,MandiFileName):
#     Price_Date = '2010-09-27'
#     pjme = df
#     split_date = '2010-10-02'
#     pjme_train = pjme.loc[pjme.index <= split_date].copy()
#     pjme_test = pjme.loc[pjme.index > split_date].copy()
#     print("---------------------pjme_train--------------------")
#     print(pjme_train["Price_Date"])
#     print("---------------------pjme_test--------------------")
#     print(pjme_test['Price_Date'])
#     print("df")
#     print(df[['Modal_Price', 'Price_Date']])
#     values = df.values
#     pyplot.plot(values)
#     y = df.Price_Date
#     x = df.drop('Price_Date',axis=1)
#     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
#     print("-----------------------------")
#     reg = xgb.XGBRegressor(n_estimators=1000)
#     reg.fit(x_train, y_train,
#             eval_set=[(x_train, y_train), (x_test, y_test)],
#
#             early_stopping_rounds=50,
#             verbose=False)
#     print("--------------------x_test--------------------")
#     print(x_test)
#     print(reg)
#     print(plot_importance(reg,height=0.9))
#     f, ax = plt.subplots(1)
#     f.set_figheight(5)
#     f.set_figwidth(15)
#     _ = df[['Modal_Price', 'Price_Date']].plot(ax=ax,
#                                                     style=['-', '.'])
#     ax.set_xbound(lower='2010-01-17', upper='2017-12-09')
#     ax.set_ylim(0, 60000)
#     plot = plt.suptitle('January 2015 Forecast vs Actuals')
#     print("----------------------------plot-----------------------")
#     print(plot)
#     print(ax.set_ylim(0, 60000))
#     print(ax.set_xbound(lower='2010-01-17', upper='2017-12-09'))
#     plot.show(plot)




MandiListForAll = []
MandiListForBajra = []
MandiListForCorriander = []
MandiListForCotton = []
MandiListForGinger = []
MandiListForGreenchilli = []
MandiListForJowar = []
MandiListForMaize = []
MandiListForOnion = []
MandiListForSoybean = []
MandiListForTomato = []
MandiListForWheat = []



# def GetMandiCopyForBajra():
#     directory = os.path.join("Datatobeprocessed/bajra/")
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             MandiListCopyForBajra.append(file)
#             # if file.endswith(".csv"):
#             #     file.split(".")
#             #     MandiListForBajra.append(file.replace(".csv", ""))
#     print("Bajra")
#     return MandiListCopyForBajra


def preprocessingdata(MandiFileName,cropname):
    # with open("Datatobeprocessed/bajra/CopyOf%s" %MandiFileName, mode='w') as employee_file:
    #     employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     with open(cropname1+'%s' %MandiFileName, 'r') as read_obj:
    #         csv_reader = reader(read_obj)
    #         header = next(csv_reader)
    #         # Check file as empty
    #         if header != None:
    #             # Iterate over each row after the header in the csv
    #             for row in csv_reader:
    #                 # row variable is a list that represents a row in csv
    #                 print(row)
    #                 # employee_writer.writerow(['John Smith', 'Accounting', 'November'])
    #                 employee_writer.writerow(row)
    fields = ['Modal Price (Rs./Quintal)', 'Price Date']

    # for i in range(0, len(MandiListCopyForBajra)):
    #     warnings.filterwarnings("ignore", category=DeprecationWarning)
    daily_Data = pd.read_csv("Datatobeprocessed/{}/{}".format(cropname,MandiFileName), skipinitialspace=True, usecols=fields,)
    print(daily_Data.head(2))
    print(daily_Data.shape)
    df = daily_Data.copy()

    print(df.columns)
    df = df.rename(index=str, columns={
            "Sl no.": "Sl_no",
            "Min Price (Rs./Quintal)": "Min_Price",
            "Price Date": "Price_Date",
            "Modal Price (Rs./Quintal)": "Modal_Price"
        })
    df.Price_Date = pd.to_datetime(df.Price_Date, errors='coerce')
    df = df.sort_values(by='Price_Date')
    df.drop_duplicates('Price_Date', inplace=True)
    return trainingmodel(df,MandiFileName,cropname)


def GetMandiid(cropId):

    client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.s73xs.mongodb.net/test")

    mydb = client["Bhav"]
    mycol = mydb["mandis"]
    selectedMandiId=""
    x = mycol.find()
    for i in x:
        for j in range(0,len(i['productId'])):
            if str(i['productId'][j]) == str(cropId):
                  selectedMandiId = str(i['_id'])
                  break
    return selectedMandiId

def GetMandiForAll(mandiname,path):
    MandiListForAll.clear()
    directory = os.path.join(path)
    for root, dirs, files in os.walk(directory):
        for file in files:
            MandiListForAll.append(file)
            break
    # GetMandiDataForAll(MandiListForAll,mandiname)
    return MandiListForAll


def GetMandiDataForAll(MandiListForAll,mandiname):
    print(MandiListForAll)
    for i in MandiListForAll:
        # filecompared1 = '{}\{}'.format(cropname1, MandiName)
        # print(filecompared1)
        print(i)
        # if file_name == filecompared1:
        with open('Datatobeprocessed/{}/{}'.format(mandiname,i), mode='w') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                with open('data/{}/{}'.format(mandiname,i), 'r') as read_obj:
                    csv_reader = reader(read_obj)
                    header = next(csv_reader)
                    # Check file as empty
                    if header != None:
                        # Iterate over each row after the header in the csv
                        for row in csv_reader:
                            # row variable is a list that represents a row in csv
                            # employee_writer.writerow(['John Smith', 'Accounting', 'November'])
                            employee_writer.writerow(row)
    MandiListForAll.clear()


def GetMandiForCorriander():
    directory = os.path.join(cropname2)
    for root, dirs, files in os.walk(directory):
        for file in files:
            MandiListForCorriander.append(file)
            # if file.endswith(".csv"):
            #     file.split(".")
            #     MandiListForBajra.append(file.replace(".csv", ""))
    return MandiListForCorriander


def GetMandiDataForCorriander():
    # for i in range(0, len(MandiListCopyForBajra)):
        # preprocessingdata(MandiListCopyForBajra[i])
    # for file_name in glob.iglob('data/BAJRA/*.csv', recursive=True):
    for i in MandiListForCorriander:
        # filecompared1 = '{}\{}'.format(cropname1, MandiName)
        # print(filecompared1)
        print(i)
        # if file_name == filecompared1:
        with open('Datatobeprocessed/CORRIANDER LEAVES/%s' %i, mode='w') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                with open('data/CORRIANDER LEAVES/%s' %i, 'r') as read_obj:
                    csv_reader = reader(read_obj)
                    header = next(csv_reader)
                    # Check file as empty
                    if header != None:
                        # Iterate over each row after the header in the csv
                        for row in csv_reader:
                            # row variable is a list that represents a row in csv
                            print(row)
                            # employee_writer.writerow(['John Smith', 'Accounting', 'November'])
                            employee_writer.writerow(row)



def GetMandiForCotton():
    directory = os.path.join(cropname3)
    for root, dirs, files in os.walk(directory):
        for file in files:
            MandiListForCotton.append(file)
            # if file.endswith(".csv"):
            #     file.split(".")
            #     MandiListForBajra.append(file.replace(".csv", ""))
    return MandiListForCotton


def GetMandiDataForCotton():
    # for i in range(0, len(MandiListCopyForBajra)):
        # preprocessingdata(MandiListCopyForBajra[i])
    # for file_name in glob.iglob('data/BAJRA/*.csv', recursive=True):
    for i in MandiListForCotton:
        # filecompared1 = '{}\{}'.format(cropname1, MandiName)
        # print(filecompared1)
        print(i)
        # if file_name == filecompared1:
        with open('Datatobeprocessed/cotton/%s' %i, mode='w') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                with open('data/cotton/%s' %i, 'r') as read_obj:
                    csv_reader = reader(read_obj)
                    header = next(csv_reader)
                    # Check file as empty
                    if header != None:
                        # Iterate over each row after the header in the csv
                        for row in csv_reader:
                            # row variable is a list that represents a row in csv
                            print(row)
                            # employee_writer.writerow(['John Smith', 'Accounting', 'November'])
                            employee_writer.writerow(row)
# def GetMandiDataForCorriander():
#     for i in range(0, len(MandiListCopyForBajra)):
#         preprocessingdata(MandiListCopyForBajra[i])
#     for file_name in glob.iglob('data/BAJRA/*.csv', recursive=True):
#         filecompared1 = '{}\{}'.format(cropname1, MandiName)
#         print(filecompared1)
#         print(file_name)
#         if file_name == filecompared1:
#             df = pd.read_csv('%s' % file_name)
#             print(df)
#             with open('employee_file.csv', mode='w') as employee_file:
#                 employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                 with open(file_name, 'r') as read_obj:
#                     csv_reader = reader(read_obj)
#                     header = next(csv_reader)
#                     # Check file as empty
#                     if header != None:
#                         # Iterate over each row after the header in the csv
#                         for row in csv_reader:
#                             # row variable is a list that represents a row in csv
#                             print(row)
#                             # employee_writer.writerow(['John Smith', 'Accounting', 'November'])
#                             employee_writer.writerow(row)
#
#
# def GetMandiDataForCotton():
#     for i in range(0, len(MandiListCopyForBajra)):
#         preprocessingdata(MandiListCopyForBajra[i])
#     for file_name in glob.iglob('data/BAJRA/*.csv', recursive=True):
#         filecompared1 = '{}\{}'.format(cropname1, MandiName)
#         print(filecompared1)
#         print(file_name)
#         if file_name == filecompared1:
#             df = pd.read_csv('%s' % file_name)
#             print(df)
#             with open('employee_file.csv', mode='w') as employee_file:
#                 employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                 with open(file_name, 'r') as read_obj:
#                     csv_reader = reader(read_obj)
#                     header = next(csv_reader)
#                     # Check file as empty
#                     if header != None:
#                         # Iterate over each row after the header in the csv
#                         for row in csv_reader:
#                             # row variable is a list that represents a row in csv
#                             print(row)
#                             # employee_writer.writerow(['John Smith', 'Accounting', 'November'])
#                             employee_writer.writerow(row)

import csv
import json


from datetime import date

today = date.today()
date = str(today).split("-")
currentdate = date[2] + "/" + date[1] + "/" + date[0]
yesterdaydate = str(int(date[2]) - 1) + "/" + date[1] + "/" + date[0]

# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath, mandiname, cropname, cropId):
    selectedmandiId = GetMandiid(cropId)
    todaysprice =GetPrice(selectedmandiId,cropId,currentdate)
    yesterdayprice = GetPrice(selectedmandiId, cropId,yesterdaydate)
    # create a dictionary
    listofdata=[]
    data = {
        "CropName":cropname,
        "Today's Price":todaysprice,
        "Yesterday's Price" : yesterdayprice,
        "CropId" : cropId,
        "MandiId" : selectedmandiId,
        "MandiName" : mandiname,
        "Data" : listofdata,
    }
    csvfile = open(csvFilePath, 'r')
    jsonfile = open(jsonFilePath, 'w')
    fieldnames = ("Date", "Lower Modal Price", "Upper Model Price")
    reader = csv.DictReader(csvfile, fieldnames)
    header = next(reader)
    if header!=None:
        for row in reader:
           listofdata.append(row)
        json.dump(data,jsonfile)


def finaldatastoredlocally(MandiList,cropname,CropId):
    for i in MandiList:
            # finaldata = preprocessingdata(i,cropname)
            # finaldata.to_csv(r'finaldatasenttouser/{}/{}'.format(cropname,i))
            # with open('finaldatasenttouser/{}/{}'.format(cropname,i), 'r') as f:
            #      my_csv_text = f.read()
            #      lines = f.readline()
            #      find_str = str(lines[0])
            #      replace_str = 'Date,Lower Modal Price,Upper Model Price'
            # new_csv_str = re.sub(find_str, replace_str, my_csv_text)

            # open new file and save
            # new_csv_path = 'finaldatasenttouser/{}/{}'.format(cropname,i)
            # with open(new_csv_path, 'w') as f:
            #            f.write(new_csv_str)
            make_json('finaldatasenttouser/{}/{}'.format(cropname,i),'finaljsonfiles/{}/{}'.format(cropname,i),i,cropname,CropId)
            break


cropname1 = 'data/BAJRA/'
cropname2 = 'data/CORRIANDER LEAVES'
cropname3 = 'data/cotton'
cropname4 = 'data/Ginger/'
cropname5 = 'data/Green Chilli'
cropname6 = 'data/Jowar'
cropname7 = 'data/Maize/'
cropname8 = 'data/Onion'
cropname9 = 'data/Soybean'
cropname10 = 'data/Tomato/'
cropname11 = 'data/Wheat'


if __name__ == '__main__':
    GetMandiForAll("BAJRA", cropname1)
    finaldatastoredlocally(MandiListForAll, "BAJRA", "5fdc9fed13b7130025988e8c")
    # GetMandiForAll("CORRIANDER LEAVES", cropname5)
    # finaldatastoredlocally(MandiListForAll, "CORRIANDER LEAVES", "5fdc9ff613b7130025988e8d")
    # GetMandiForAll("cotton", cropname2)
    # finaldatastoredlocally(MandiListForAll, "cotton", "5fdc9ffe13b7130025988e8e")
    # GetMandiForAll("Ginger",cropname3)
    # finaldatastoredlocally(MandiListForAll, "Ginger", "5fdca00613b7130025988e8f")
    # GetMandiForAll("Green Chilli",cropname5)
    # finaldatastoredlocally(MandiListForAll, "Green Chilli", "5fdc9ed313b7130025988e85")
    # GetMandiForAll("Jowar",cropname6)
    # finaldatastoredlocally(MandiListForAll, "Jowar", "5fdc9ede13b7130025988e86")
    # GetMandiForAll("Maize",cropname7)
    # finaldatastoredlocally(MandiListForAll, "Maize", "5fdc9ee813b7130025988e87")
    # GetMandiForAll("Onion",cropname8)
    # finaldatastoredlocally(MandiListForAll, "Onion", "5fdc9ef513b7130025988e88")
    # GetMandiForAll("Soybean",cropname9)
    # finaldatastoredlocally(MandiListForAll, "Soybean", "5fdc9f0b13b7130025988e89")
    # GetMandiForAll("Tomato",cropname10)
    # finaldatastoredlocally(MandiListForAll, "Tomato", "5fdc9f1713b7130025988e8a")
    # GetMandiForAll("Wheat",cropname11)
    # finaldatastoredlocally(MandiListForAll, "Wheat", "5fdc9f2013b7130025988e8b")

    # GetMandiDataForBajra()
    # GetMandiForCorriander()
    # GetMandiDataForCorriander()
    # GetMandiForCotton()
    # GetMandiDataForCotton()
    # finaldatastoredlocally(MandiListForBajra,"BAJRA","5fdc9fed13b7130025988e8c")
    # finaldatastoredlocally(MandiListForCorriander,"CORRIANDER LEAVES","5fdc9ff613b7130025988e8d")
    # finaldatastoredlocally(MandiListForCotton,"cotton","5fdc9ffe13b7130025988e8e")




