from flask import Flask, render_template, request, session, redirect, flash, jsonify
from src import backend  # Importing backend module
import pickle  # Importing pickle for object serialization
import qrcode  # Importing qrcode for QR code generation
import os  # Importing os for miscellaneous operating system interfaces

# Creating a Flask application
app = Flask(__name__, template_folder="../templates", static_folder="../static")
# Generating a secret key for session management
app.secret_key = os.urandom(16).hex()


def login_status():
    """
    Check the login status of the user.

    Returns:
    - tuple: A tuple containing username and login status.
    """
    try:
        username = session["username"]
    except KeyError:
        username = False
    try:
        logged_in = session["logged_in"]
    except KeyError:
        logged_in = False

    return username, logged_in


def recall(username):
    """
    Recall user data from a pickled file.

    Parameters:
    - username (str): The username of the user.

    Returns:
    - User or False: The recalled user object or False if retrieval fails.
    """
    try:
        with open(f"./data/{username}.bin", "rb") as file:
            user = pickle.load(file)
            return user
    except:
        return False


def save(user):
    """
    Save user data into a pickled file.

    Parameters:
    - user (User): The user object to be saved.
    """
    with open(f"./data/{user.username}.bin", "wb") as file:
        pickle.dump(user, file)


def sort_results(results):
    """
    Sort search results by views and username.

    Parameters:
    - results (list): List of Credential objects.

    Returns:
    - list: Sorted list of Credential objects.
    """
    return sorted(results, key=lambda x: (x.views, x.username), reverse=True)


def get_version():
    """
    Get the current version of the application.

    Returns:
    - str: The current version of the application.
    """
    try:
        count = os.popen("git rev-list --count master").read().strip()
    except:
        count = 0
    version = [char for char in str(count)]
    return ".".join(version)


@app.route("/")
def index():
    """
    Render the index page.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username and logged_in:
        user = recall(username)
        creds = sort_results(user.list_creds())[:10]
        return render_template("index.html", username=username, creds=creds)
    elif username:
        return redirect("/totp-verify")
    return render_template("index.html")


@app.route("/version")
def version():
    """
    Get the current version of the application.

    Returns:
    - str: JSON response containing the application version.
    """
    return jsonify({"version": get_version()})


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.

    Returns:
    - str: Rendered HTML template.
    """
    login_error = False
    if request.method == "POST":
        username = str(request.form["username"]).lower()
        password = request.form["password"]
        if os.path.exists(f"./data/{username}.bin"):
            user = recall(username)
            if user.verify_password(password):
                session["username"] = username
                return redirect("/totp-verify")
            else:
                login_error = True
        else:
            login_error = True
    return render_template(
        "login.html", login_page=True, title="Login", error=login_error
    )


@app.route("/signup", methods=["GET", "POST"])
def new_user():
    """
    Handle user signup.

    Returns:
    - str: Rendered HTML template.
    """
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
            return redirect("/totp-enroll")
    return render_template(
        "signup.html", login_page=True, title="Create Account", error=error
    )


@app.route("/totp-enroll", methods=["GET", "POST"])
def totp_enroll():
    """
    Handle TOTP enrollment.

    Returns:
    - str: Rendered HTML template.
    """
    error = False
    username, logged_in = login_status()
    if username and request.method == "POST":
        user = recall(username)
        code = request.form["code"]
        if user.totp_verify(str(code)):
            session["logged_in"] = True
            os.remove(f"./static/private/{username}")
            return redirect("/")
        else:
            return render_template(
                "totp-enroll.html",
                login_page=True,
                title="Enroll 2FA",
                error=True,
                image_name=username,
            )
    elif username:
        user = recall(username)
        qr = qrcode.make(user.totp_get())
        if not os.path.exists("./static/private"):
            os.mkdir("./static/private")
        qr.save("./static/private/" + username)
        return render_template(
            "totp-enroll.html",
            login_page=True,
            title="Enroll 2FA",
            error=error,
            image_name=username,
        )
    else:
        return redirect("/")

@app.route("/totp-verify", methods=["GET", "POST"])
def totp_verify():
    """
    Handle TOTP verification.

    Returns:
    - str: Rendered HTML template.
    """
    error = False
    username, logged_in = login_status()
    if username and logged_in:
        return redirect("/")
    elif username:
        if request.method == "POST":
            code = request.form["code"]
            user = recall(username)
            if user.totp_verify(str(code)):
                session["logged_in"] = True
                return redirect("/")
            else:
                return render_template(
                    "totp-verify.html", login_page=True, title="Verify 2FA", error=True
                )
        return render_template(
            "totp-verify.html", login_page=True, title="Verify 2FA", error=error
        )
    return redirect()


@app.route("/reset-password")
def password_reset():
    """
    Render the password reset page.

    Returns:
    - str: Rendered HTML template.
    """
    return render_template("/reset-password.html", login_page=True)


@app.route("/list-logins")
def list_logins():
    """
    Render the list of saved logins page.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username and logged_in:
        user = recall(username)
        creds = sort_results(user.list_creds())
        return render_template(
            "list-logins.html", title="Saved Accounts", username=username, creds=creds
        )
    elif username:
        return redirect("/totp-verify")
    else:
        return redirect("/login")


@app.route("/new-login", methods=["GET", "POST"])
def new_login():
    """
    Handle addition of new login credentials.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username and logged_in:
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
    elif username:
        return redirect("/totp-verify")
    else:
        return redirect("/login")

@app.route("/search-logins")
def search_login():
    """
    Handle searching for login credentials.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username:
        query = request.args.get("query")
        results = []
        if query:
            user = recall(username)
            results = user.query(query)
        return render_template(
            "search.html", title="Search", username=username, creds=results
        )
    elif username:
        return redirect("/totp-verify")
    else:
        return redirect("/login")


@app.route("/view-login")
def view_login():
    """
    Render the page to view a specific login credential.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username and logged_in:
        id = request.args.get("id")
        if id:
            user = recall(username)
            creds = user.list_creds()
            result = None
            for cred in creds:
                if id == cred.id:
                    result = cred
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
    elif username:
        return redirect("/totp-verify")
    else:
        redirect("/login")


@app.route("/edit-login", methods=["GET", "POST"])
def edit_login():
    """
    Handle editing of a login credential.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username and logged_in:
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
    elif username:
        return redirect("/totp-verify")
    else:
        return redirect("/login")


@app.route("/delete-login")
def delete_login():
    """
    Handle deletion of a login credential.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username and logged_in:
        id = request.args.get("id")
        confirmed = request.args.get("confirmed")
        if id and confirmed:
            user = recall(username)
            user.del_cred(id)
            save(user)
            return redirect("/list-logins")
        elif id and not confirmed:
            return render_template(
                "delete-login.html", title="Delete Account", login_page=True, id=id
            )
        else:
            return redirect("/list-logins")
    elif username:
        return redirect("/totp-verify")
    else:
        return redirect("/login")


@app.route("/password-generator")
def password_generator():
    """
    Render the password generator page.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username:
        return render_template(
            "password-generator.html", title="Password Generator", username=username
        )
    else:
        return redirect("/login")


@app.route("/settings")
def settings():
    """
    Render the settings page.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username and logged_in:
        return render_template(
            "settings.html", title="Settings", username=username, verion=version
        )
    elif username:
        return redirect("/totp-verify")
    else:
        return redirect("/login")


@app.route("/profile")
def profile():
    """
    Render the user's profile page.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username and logged_in:
        return render_template(
            "profile.html",
            title=f"{username.capitalize()}'s Profile",
            username=username,
        )
    elif username:
        return redirect("/totp-verify")
    else:
        return redirect("/login")


@app.route("/profile/change-password", methods=["GET", "POST"])
def change_password():
    """
    Handle changing the user's password.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    if username and logged_in:
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
    elif username:
        return redirect("/totp-verify")
    else:
        return redirect("/login")


@app.route("/profile/delete")
def delete_profile():
    """
    Handle deletion of the user's profile.

    Returns:
    - str: Rendered HTML template.
    """
    username, logged_in = login_status()
    confirmed = request.args.get("confirmed")
    if username and logged_in and confirmed:
        os.remove(f"./data/{username}.bin")
        session.clear()
        return redirect("/")
    elif username and logged_in:
        return render_template(
            "delete-profile.html", title="Delete Profile", login_page=True
        )
    else:
        return redirect("/login")


@app.route("/logout")
def logout_user():
    """
    Handle user logout.

    Returns:
    - str: Redirect to the home page.
    """
    session.pop("username", default=None)
    session.pop("logged_in", default=None)
    return redirect("/")
