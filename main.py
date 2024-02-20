from src.frontend import app
import os

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 8080

    clear = lambda: os.system("clear") if os.name == "posix" else os.system("cls")
    clear()
    if not os.path.exists("./data"):
        os.mkdir("./data")

    app.run(host=HOST, port=PORT, debug=True)
