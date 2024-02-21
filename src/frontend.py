from flask import Flask, render_template, request, session, redirect, flash, jsonify
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


def sort_results(results, sort_by=None, descending=False):
    return sorted(results, key=lambda x: (x.views, x.username), reverse=(True, False))


def get_version():
    try:
        count = os.popen("git rev-list --count master").read().strip()
    except:
        count = 0
    version = [char for char in str(count)]
    return ".".join(version)


@app.route("/")
def index():
    username = login_status()
    if username:
        user = recall(username)
        creds = sort_results(user.list_creds())[:10]
        return render_template("index.html", username=username, creds=creds)
    return render_template("index.html")


@app.route("/version")
def version():
    return jsonify({"version": get_version()})


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

@app.route("/password-reset")
def password_reset():
    return jsonify("Coming soon.")

@app.route("/list-logins")
def list_logins():
    username = login_status()
    if username:
        user = recall(username)
        creds = sort_results(user.list_creds())
        return render_template(
            "list-logins.html", title="Saved Accounts", username=username, creds=creds
        )
    else:
        return redirect("/login")


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
        return render_template("new-login.html", title="Creating...", username=username)
    else:
        return redirect("/login")


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


@app.route("/view-login")
def view_login():
    username = login_status()
    if username:
        id = request.args.get("id")
        if id:
            user = recall(username)
            creds = user.list_creds()
            result = None
            for cred in creds:
                if id == cred.id:
                    result = cred
                    print(result.views)
                    result.views += 1
                    user.del_cred(id)
                    user.add_cred(
                        result.username,
                        result.password,
                        result.email,
                        result.website,
                        result.notes,
                        result.views,
                    )
                    save(user)
                    break

        return render_template(
            "view-login.html", title="Viewing...", username=username, cred=result
        )
    else:
        redirect("/login")


@app.route("/edit-login", methods=["GET", "POST"])
def edit_login():
    username = login_status()
    if username:
        id = request.args.get("id")
        if id:
            user = recall(username)
            creds = user.list_creds()
            result = None
            for cred in creds:
                if id == cred.id:
                    result = cred
                    break
        if request.method == "POST" and id:
            _username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
            website = request.form["website"]
            notes = request.form["notes"]
            user.del_cred(id)
            user.add_cred(_username, password, email, website, notes, result.views)
            save(user)
            return redirect("/list-logins")
        return render_template(
            "edit-login.html", title="Editing...", username=username, cred=result
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


@app.route("/password-generator")
def password_generator():
    username = login_status()
    if username:
        return render_template(
            "password-generator.html", title="Password Generator", username=username
        )
    else:
        return redirect("/login")


### SETTINGS
@app.route("/settings")
def settings():
    username = login_status()
    if username:
        return render_template(
            "settings.html", title="Settings", username=username, verion=version
        )
    else:
        return redirect("/login")


@app.route("/profile")
def profile():
    username = login_status()
    if username:
        return render_template("profile.html", title=f"{username.capitalize()}'s Profile", username=username)
    else:
        return redirect("/login")


@app.route("/profile/change-password", methods=["GET", "POST"])
def change_password():
    username = login_status()
    if username:
        error = False
        if request.method == "POST":
            current = request.form["password"]
            new = request.form["password1"]
            new1 = request.form["password2"]

            user = recall(username)
            if not user.verify_password(current):
                error = "Password incorrect"
            elif new != new1:
                error = "Passwords must match"
            else:
                user.change_password(new)
                save(user)
                return redirect("/profile")
        return render_template(
            "change-password.html",
            title="Change Password",
            login_page=True,
            error=error,
        )
    else:
        return redirect("/login")


### PROFILE/DELETE


@app.route("/logout")
def logout_user():
    session.pop("username", default=None)
    return redirect("/")
