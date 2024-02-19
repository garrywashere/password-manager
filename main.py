from src import frontend
import os

clear = lambda: os.system("clear") if os.name == "posix" else os.system("cls")

if __name__ == "__main__":
    clear()

    if not os.path.exists("./data"):
        os.mkdir("./data")

    frontend.app.run(host="127.0.0.1", port=8080, debug=True)
