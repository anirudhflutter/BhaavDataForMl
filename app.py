from flask import jsonify,Flask
from flask import request
import future_prediction
import pandas as pd
import json
import os
app = Flask(__name__)

# def getMandiDataCropWise():
GetBajraMandiData = future_prediction.GetMandiForBajra()
GetCorrianderMandiData = future_prediction.GetMandiForCorriander()
GetCottonMandiData = future_prediction.GetMandiForCotton()
FinalDataSentToUser=[]


@app.route('/getuserselectedmandi')
def getuserselectedmandi():
    MandiName = request.args.get('MandiName')
    if MandiName == "":
        return jsonify({"Message" : "Please provide MandiName"})
    else:
        EnteredMandi = MandiName+".csv"
        FinalDataSentToUser.clear()
        for i in GetBajraMandiData:
            if i==EnteredMandi:
                f = open("finaljsonfiles/BAJRA/{}".format(EnteredMandi))
                data = json.load(f)
                FinalDataSentToUser.append(data)
        for i in GetCorrianderMandiData:
            if i==EnteredMandi:
                f = open("finaljsonfiles/CORRIANDER LEAVES/{}".format(EnteredMandi))
                data = json.load(f)
                FinalDataSentToUser.append(data)
        for i in GetCottonMandiData:
            if i==EnteredMandi:
                f = open("finaljsonfiles/cotton/{}".format(EnteredMandi))
                data = json.load(f)
                FinalDataSentToUser.append(data)

        return jsonify({
                "data" : FinalDataSentToUser
    })


if __name__ == '__main__':
    app.run(port=80)
