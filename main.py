from src import frontend
import os

# Modify these values to change server settings
HOST = "127.0.0.1"
PORT = 8080


clear = lambda: os.system("clear") if os.name == "posix" else os.system("cls")

if __name__ == "__main__":
    clear()

    if not os.path.exists("./data"):
        os.mkdir("./data")

    frontend.app.run(host=HOSTNAME, port=PORT, debug=True)
