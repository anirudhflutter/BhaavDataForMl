from flask import jsonify,Flask
from flask import request
import future_prediction
import pandas as pd
import json
import os
app = Flask(__name__)

FinalDataSentToUser=[]

def GetData(enteredmandi,crop,mandipath):
    Data = future_prediction.GetMandiForAll(crop,mandipath)
    for i in Data:
        if i == enteredmandi:
            f = open("finaljsonfiles/{}/{}".format(crop,enteredmandi))
            data = json.load(f)
            FinalDataSentToUser.append(data)


@app.route('/getuserselectedmandi')
def getuserselectedmandi():
    MandiName = request.args.get('MandiName')
    if MandiName == "":
        return jsonify({"Message" : "Please provide MandiName"})
    else:
        EnteredMandi = MandiName+".csv"
        FinalDataSentToUser.clear()
        GetData(EnteredMandi,"BAJRA",future_prediction.cropname1)
        GetData(EnteredMandi, "CORRIANDER LEAVES",future_prediction.cropname2)
        GetData(EnteredMandi, "cotton",future_prediction.cropname3)
        GetData(EnteredMandi, "Ginger",future_prediction.cropname4)
        GetData(EnteredMandi, "Green Chilli",future_prediction.cropname5)
        GetData(EnteredMandi, "Jowar",future_prediction.cropname6)
        GetData(EnteredMandi, "Maize",future_prediction.cropname7)
        GetData(EnteredMandi, "Onion",future_prediction.cropname8)
        GetData(EnteredMandi, "Soybean",future_prediction.cropname9)
        GetData(EnteredMandi, "Tomato",future_prediction.cropname10)
        GetData(EnteredMandi, "Wheat",future_prediction.cropname11)

        return jsonify({
                "data" : FinalDataSentToUser
    })


port = int(os.environ.get("PORT", 5000))


if __name__ == '__main__':
    app.run(debug=True, host='192.168.29.54', port=port)
