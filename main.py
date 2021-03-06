import glob
import csv
import pandas as pd
import os
import requests
import pymongo
import future_prediction


mandiname = 'Ahmednagar'
cropname1 = 'data/BAJRA'
cropname2 = 'data/CORRIANDER LEAVES'
cropname3 = 'data/cotton'
filecompared2 = '{}\{}'.format(cropname2, mandiname)

fields = ['Modal_Price', 'Price_Date']
MandiListForBajra = []
MandiListForCorriander = []
MandiListForCotton = []

CropListName = []
CropListId = []


def GetMandiForBajra():
    directory = os.path.join(cropname1)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                file.split(".")
                MandiListForBajra.append(file.replace(".csv", ""))
    return MandiListForBajra


def GetMandiForCorriander():
    directory = os.path.join(cropname2)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                file.split(".")
                MandiListForCorriander.append(file.replace(".csv", ""))
    return MandiListForCorriander


def GetMandiForCotton():
    directory = os.path.join(cropname3)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                file.split(".")
                MandiListForCotton.append(file.replace(".csv", ""))
    return MandiListForCotton


def GetProductNameAndId():

    client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.s73xs.mongodb.net/test")

    mydb = client["Bhav"]
    mycol = mydb["products"]

    x = mycol.find()
    for i in x:
        print(i)
        CropListName.append(i['productName'])
        CropListId.append(i['_id'])



def SendWholeDataToMonil(mandiname, productid):
    print("inside service function")
    print(mandiname)
    print(productid)
    mandi = mandiname.replace(".csv","")
    url = 'https://bhav003.herokuapp.com/api/mandi/addMandi'
    myobj = {
        "MandiName": str(mandi),
        "productId": str(productid),
        "State": "5fabbe4fd652567fdb848e3a",
    }
    x = requests.post(url, data=myobj)
    print(x)


mandilistforall = []


def GetMandiForAll(cropname):
    directory = os.path.join(cropname)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                file.split(".")
                mandilistforall.append(file.replace(".csv", ""))
    return mandilistforall


def main():
    # GetMandiForCorriander()
    # GetMandiForCotton()
    GetProductNameAndId()
    for i in range(0,len(CropListName)):
        if CropListName[i]=='Bajra':
            for j in range(0, len(future_prediction.GetMandiForAll("Bajra",future_prediction.cropname1))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Bajra",future_prediction.cropname1)[j]), CropListId[i])
        if CropListName[i] == 'Corriander Leaves':
            for j in range(0, len(future_prediction.GetMandiForAll("Corriander Leaves",future_prediction.cropname2))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Corriander Leaves",future_prediction.cropname2)[j]), CropListId[i])
        if CropListName[i] == 'Cotton':
            for j in range(0, len(future_prediction.GetMandiForAll("Cotton",future_prediction.cropname3))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Cotton",future_prediction.cropname3)[j]), CropListId[i])
        if CropListName[i] == 'Ginger':
            for j in range(0, len(future_prediction.GetMandiForAll("Ginger",future_prediction.cropname4))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Ginger",future_prediction.cropname4)[j]), CropListId[i])
        if CropListName[i] == 'Green Chilli':
            for j in range(0, len(future_prediction.GetMandiForAll("Green Chilli",future_prediction.cropname5))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Green Chilli",future_prediction.cropname5)[j]), CropListId[i])
        if CropListName[i] == 'Jowar':
            for j in range(0, len(future_prediction.GetMandiForAll("Jowar",future_prediction.cropname6))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Jowar",future_prediction.cropname6)[j]), CropListId[i])
        if CropListName[i] == 'Maize':
            for j in range(0, len(future_prediction.GetMandiForAll("Maize",future_prediction.cropname7))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Maize",future_prediction.cropname7)[j]), CropListId[i])
        if CropListName[i] == 'Onion':
            for j in range(0, len(future_prediction.GetMandiForAll("Onion",future_prediction.cropname8))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Onion",future_prediction.cropname8)[j]), CropListId[i])
        if CropListName[i] == 'Soybean':
            for j in range(0, len(future_prediction.GetMandiForAll("Soybean",future_prediction.cropname9))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Soybean",future_prediction.cropname9)[j]), CropListId[i])
        if CropListName[i] == 'Tomato':
            for j in range(0, len(future_prediction.GetMandiForAll("Tomato",future_prediction.cropname10))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Tomato",future_prediction.cropname10)[j]), CropListId[i])
        if CropListName[i] == 'Wheat':
            for j in range(0, len(future_prediction.GetMandiForAll("Wheat",future_prediction.cropname11))):
                SendWholeDataToMonil(str(future_prediction.GetMandiForAll("Wheat",future_prediction.cropname11)[j]), CropListId[i])
    # for file_name in glob.iglob('data/BAJRA/*.csv',recursive=True):
    #     filecompared1 = '{}/{}'.format(cropname1,mandiname)
    #     if file_name == filecompared1 + '.csv':
    #         df = pd.read_csv(r'%s' %file_name)
    #         print(df)
    #         newdf = df.iloc[1:]
    #         newdf.rename(index=str, columns={
    #             "Sl no.": "Sl_no",
    #             "Min Price (Rs./Quintal)": "Min_Price",
    #             "Price Date": "Price_Date",
    #             "Modal Price (Rs./Quintal)": "Modal_Price"
    #         })
    #
    #         print(newdf.head(20))
    #         newdf.to_csv("wheat2.csv", sep=',')
    #     print(file_name)
    #
    # for file_name in glob.iglob('data/CORRIANDER LEAVES/**/*.csv',recursive=True):
    #     filecompared2 = '{}/{}'.format(cropname2,mandiname)
    #     if file_name == filecompared2 + '.csv':
    #         print(file_name)
    #
    # for file_name in glob.iglob('data/cotton/**/*.csv',recursive=True):
    #     filecompared3 = '{}/{}'.format(cropname3,mandiname)
    #     if file_name == filecompared3 + '.csv':
    #         print(file_name)


if __name__ == "__main__":
    main()
