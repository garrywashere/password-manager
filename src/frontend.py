from flask import Flask, render_template, request, session, redirect, flash
from src import backend
import pickle, os

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "4369307056126f5f09ced025"


# Index
@app.route("/")
def index():
    return render_template("index.html", title="Welcome")


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

            return redirect("/")

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
                session["logged_in"], session["username"] = True, username
                return "login succeeded", 200
            else:
                return render_template("user-login.html", error="Password incorrect")

    return render_template("user-login.html", title="Login")


@app.route("/user/logout")
def logout_user():
    session.pop("logged_in", default=None)
    session.pop("username", default=None)
    return redirect("/")


# New Login
@app.route("/login/new", methods=["GET", "POST"])
def new_login():
    try:
        session_user = session["username"]
        logged_in = session["logged_in"]
    except KeyError:
        return redirect("/user/login")
    if logged_in and session_user:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
            website = request.form["website"]
            notes = request.form["notes"]

            with open(f"./data/{session_user}.bin", "rb") as file:
                user = pickle.load(file)

            user.add_login(username, password, email, website, notes)

            with open(f"./data/{session_user}.bin", "wb") as file:
                pickle.dump(user, file)

            return "login added", 200

        return render_template("login-new.html", title="New Login")

    else:
        return redirect("/user/login")


# Search Login
@app.route("/logins/search", methods=["GET", "POST"])
def search_login():
    try:
        session_user = session["username"]
        logged_in = session["logged_in"]
    except KeyError:
        return redirect("/user/login")
    if logged_in and session_user:
        if request.method == "POST":
            search = request.form["search"]

            with open(f"./data/{session_user}.bin", "rb") as file:
                user = pickle.load(file)

            results = user.query_login(search)

            return render_template("login-search.html", results=results)
        return render_template("login-search.html")
    else:
        return redirect("/user/login")


# See all logins
@app.route("/logins/list")
def list_logins():
    try:
        logged_in = session["logged_in"]
        username = session["username"]
    except KeyError:
        return redirect("/user/login")
    if logged_in and username:
        with open(f"./data/{username}.bin", "rb") as file:
            user = pickle.load(file)
        logins = user.list_logins()
        return render_template("login-list.html", logins=logins)
