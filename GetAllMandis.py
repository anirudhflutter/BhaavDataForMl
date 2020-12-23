import pymongo
import os
from flask import jsonify, Flask
from flask import request

GetAllMandis = []

app = Flask(__name__)


def getAllMandis():
    client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.s73xs.mongodb.net/test")

    # Database Name
    db = client["Bhav"]

    # Collection Name
    col = db["mandis"]

    x = col.find()

    for data in x:
        mandiname = str(data["MandiName"]).replace(".csv", "")
        mandiid = str(data["_id"])
        if mandiname not in GetAllMandis:
            GetAllMandis.append({
                "mandiname":mandiname,
                "id":mandiid
            })
    return mandiname


@app.route('/getAllMandis')
def AllMandis():
    return jsonify({"Data": GetAllMandis})


if __name__ == '__main__':
    getAllMandis()
    app.run(debug=True, host='192.168.29.54')
