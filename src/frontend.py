from flask import Flask, render_template, request
from src import backend
import pickle, os, argon2

app = Flask(__name__, template_folder="../templates", static_folder="../static")


# New User
@app.route("/user/new", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        username = request.form["username"]
        password = hasher.hash(request.form["password"])

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

# New Login

# Search Login

# See all logins
