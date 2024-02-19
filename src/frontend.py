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


def recall(username):
    with open(f"./data/{username}.bin", "rb") as file:
        user = pickle.load(file)
    return user


def save(user):
    with open(f"./data/{user.username}.bin", "wb") as file:
        pickle.dump(user, file)


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
            user = recall(username)

            if user.verify_password(password):
                session["username"] = username
                return redirect("/")

            else:
                login_error = True
        else:
            login_error = True
    return render_template(
        "login.html", login_page=True, title="Login", error=login_error
    )


@app.route("/signup", methods=["GET", "POST"])
def new_user():
    error = False
    if request.method == "POST":
        username = str(request.form["username"]).lower()
        password = request.form["password"]
        password2 = request.form["password2"]

        if password != password2:
            error = "Passwords don't match"

        elif os.path.exists(f"./data/{username}.bin"):
            error = "Username taken"
        else:
            new_user = backend.User(username, password)
            save(new_user)

            session["username"] = username
            return redirect("/")

    return render_template(
        "signup.html", login_page=True, title="Create Account", error=error
    )


@app.route("/logout")
def logout_user():
    session.pop("username", default=None)
    return redirect("/")


@app.route("/new-login", methods=["GET", "POST"])
def new_login():
    username = login_status()
    if username:
        if request.method == "POST":
            _username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
            website = request.form["website"]
            notes = request.form["notes"]

            user = recall(username)

            user.add_cred(_username, password, email, website, notes)

            save(user)

            return redirect("/list-logins")

        return render_template("new-login.html", title="New Login", username=username)
    else:
        return redirect("/login")


# See all logins
@app.route("/list-logins")
def list_logins():
    username = login_status()
    if username:
        user = recall(username)

        creds = user.list_creds()

        return render_template(
            "list-logins.html", title="Logins", username=username, creds=creds
        )
    else:
        return redirect("/login")


@app.route("/delete-login")
def delete_login():
    username = login_status()
    if username:
        id = request.args.get("id")

        user = recall(username)

        user.del_cred(id)

        save(user)

        return redirect("/list-logins")

    else:
        redirect("/login")


@app.route("/search-logins")
def search_login():
    username = login_status()
    if username:
        query = request.args.get("query")

        results = []
        if query:
            user = recall(username)
            results = user.query(query)

        return render_template(
            "search.html", title="Search", username=username, creds=results
        )
    else:
        redirect("/login")