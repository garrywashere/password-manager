from flask import Flask, render_template, request, session, redirect, flash
from src import backend
import pickle, os

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "4369307056126f5f09ced025"


def login_status():
    try:
        username = session["username"]
        return username
    except KeyError:
        return False


@app.route("/")
def index():
    username = login_status()
    if username:
        return render_template("index.html", username=username)
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    login_error = False
    if request.method == "POST":
        username = str(request.form["username"]).lower()
        password = request.form["password"]

        if os.path.exists(f"./data/{username}.bin"):
            print("exists")
            with open(f"./data/{username}.bin", "rb") as file:
                user = pickle.load(file)

            if user.verify_password(password):
                print("password worked")
                session["username"] = username
                return redirect("/")

            else:
                print("password didn't work")
                login_error = True
        else:
            print("file not found")
            login_error = True
    return render_template(
        "login.html", login_page=True, title="Login", error=login_error
    )


@app.route("/signup", methods=["GET", "POST"])
def new_user():
    error = False
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]

        if password != password2:
            error = "Passwords don't match"

        elif os.path.exists(f"./data/{username}.bin"):
            error = "Username taken"
        else:
            new_user = backend.User(username, password)
            with open(f"./data/{username}.bin", "wb") as file:
                pickle.dump(new_user, file)

            session["username"] = username
            return redirect("/")

    return render_template(
        "signup.html", login_page=True, title="Create Account", error=error
    )


@app.route("/logout")
def logout_user():
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

            return redirect("/")

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
