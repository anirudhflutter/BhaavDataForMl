import pymongo

datafound=False

def getPrice(selectedmandiId,cropid,date):
    client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.s73xs.mongodb.net/test")

    # Database Name
    db = client["Bhav"]

    # Collection Name
    col = db["updateproductprices"]

    x = col.find()

    for data in x:
        datamandiid = data["mandiId"]
        datacropid = data["productId"]
        currentdate = data["date"]
        if datamandiid == selectedmandiId & datacropid == cropid & currentdate == date:
            datafound = True
            print("yes data found")
            return data["highestPrice"]
            break
    if datafound == False:
        print("data not found")
        return ""

