from flask import jsonify,Flask
from flask import request

MandiName = ""

app = Flask(__name__)

@app.route('/getuserselectedmandi')
def getuserselectedmandi():
    MandiName = request.args.get('MandiName')
    if MandiName == "":
        return jsonify({"Message" : "Please provide MandiName"})
    else:
        print(MandiName)
        return jsonify({
            "MandiName" : '{}'.format(MandiName),
            "Message": "Got Mandi Successfully"})


if __name__ == '__main__':
    app.run(debug=True)
