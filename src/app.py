from flask import Flask
from flask import render_template, jsonify, url_for, redirect, request, flash, get_flashed_messages
import bcrypt
import os

import json
import pathlib


APPNAME : str = "Tournament creator"
FILE_USERS: str = "src/users.json"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(40)


datafile = pathlib.Path("src/data.json")
with open(datafile, "r") as _file:
    data = json.load(_file)



@app.route("/")
def index():
    matches_data = data_json()
    return render_template("index.html", title=APPNAME, matches=matches_data.json)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", title=APPNAME+" - Login")


@app.route("/register", methods=["GET", "POST"])
def register():    
    return render_template("register.html", title=APPNAME+" - Register")


@app.route("/handle_registration", methods=["GET", "POST"])
def handle_registration():
    username = request.form["username"]
    email = request.form["email"]
    password = bcrypt.hashpw(str(request.form["password"]).encode('utf-8'), bcrypt.gensalt(12))

    with open(FILE_USERS, "r") as _file:
        users = json.load(_file)

    error = False
    for user in users:
        if users[user]["username"] == username:
            flash("Username is already taken.")
            error = True
        if users[user]["email"] == email:
            flash(f"You already have an account with this email. Please login: {url_for('login')}")
            error = True

    if error:
        print(get_flashed_messages())
        return redirect(url_for("register"))
    
    elif not error:
        return redirect(url_for("dashboard"))
    
    else:
        flash("An unknown error has occured.")
        return redirect(url_for("register"))

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", title=APPNAME+" - Dashboard")


@app.route("/data_json")
def data_json():
    return jsonify(data)


@app.route("/data_update")
def data_update():
    global data, datafile
    with open(datafile, "r") as _file:
        data = json.load(_file)

    return "File reloaded!"

@app.route("/games")
def games():
    return "Types of games"

@app.route("/games/soccer")
@app.route("/games/football")
def football():
    return "Football"


@app.route("/get", defaults={"name": "NONE"})
@app.route("/get/<int:name>")
def get(name):
    name = int(name)
    #_id = request.args.get("id", type=int)
    for match in data:
        print(match)
        if match["id"] == name:
            print("in")
            return render_template("match_by_id.html", title=APPNAME, matches=[match])
        
    return f"No result found for match with id: {name}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)