import pymongo

price = 0


# Python program to find an element x
# in a sorted array using Exponential Search

# A recurssive binary search function returns
# location of x in given array arr[l..r] is
# present, otherwise -1

def binarySearch(arr, x,y,z):
    l = 0
    r = len(arr)
    while (l <= r):
        m = l + ((r - l) // 2)
        print(str(arr[m]["mandiId"]))
        print(str(arr[m]["productId"]))
        res = (x == str(arr[m]["mandiId"]) and y == str(arr[m]["productId"]) and z == str(arr[m]["date"]))

        # Check if x is present at mid
        if (res == True):
            return arr[m-1]["highestPrice"]

        # If x greater, ignore left half
        if (res > 0):
            l = m + 1

        # If x is smaller, ignore right half
        else:
            r = m - 1

    return -1


# Returns the position of first
# occurrence of x in arra


MandisList=[]


def getprice(selectedmandiId,selectedcropId,date):
    client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.s73xs.mongodb.net/test")

    # Database Name
    db = client["Bhav"]

    # Collection Name
    col = db["updateproductprices"]

    x = col.find()

    for data in x:
        MandisList.append(data)
        # MandisList.append({
        #     "mandiId" : str(data["mandiId"]),
        #
        # })
        # datamandiid = str(data["mandiId"])
        # datacropid = str(data["productId"])
        # currentdate = data["date"]
    result = binarySearch(MandisList,selectedmandiId,selectedcropId,date)
    print(result)


if __name__ == '__main__':
    getprice("5fddf5a07e446273391d34f3","5fdc9ede13b7130025988e86")