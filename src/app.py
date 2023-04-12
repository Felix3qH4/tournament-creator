from flask import Flask
from flask import render_template, jsonify
import json
import pathlib


APPNAME : str = "Tournament creator"


app = Flask(__name__)

datafile = pathlib.Path("src/data.json")
with open(datafile, "r") as _file:
    data = json.load(_file)



@app.route("/")
def index():
    matches_data = data_json()
    return render_template("index.html", title=APPNAME, matches=matches_data.json)


@app.route("/data_json")
def data_json():
    return jsonify(data)


@app.route("/data_update")
def data_update():
    global data, datafile
    with open(datafile, "r") as _file:
        data = json.load(_file)

    return "File reloaded!"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)