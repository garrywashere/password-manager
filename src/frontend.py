from flask import Flask, render_template, request
from src import backend
import pickle, os

app = Flask(__name__, template_folder="../templates", static_folder="../static")


# New User
@app.route("/user/new", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if os.path.exists(f"./data/{username}.bin"):
            return render_template("user-new.html", error="Username Taken")
        else:
            new_user = backend.User(username, password)
            with open(f"./data/{username}.bin", "wb") as file:
                pickle.dump(new_user, file)
            print("user added")

            return "user added", 200

    return render_template("user-new.html", title="New User")


# Login
@app.route("/user/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not os.path.exists(f"./data/{username}.bin"):
            return render_template("user-login.html", error="Username not recognised")
        else:
            with open(f"./data/{username}.bin", "rb") as file:
                user = pickle.load(file)
            if user.verify_password(password):
                return "login succeeded", 200
            else:
                return render_template("user-login.html", error="Password incorrect")

    return render_template("user-login.html", title="Login")


# New Login

# Search Login

# See all logins
