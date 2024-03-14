# Import the Flask app from the frontend module
from src.frontend import app
import os

if __name__ == "__main__":
    # Define the host and port for running the Flask app
    HOST = "127.0.0.1"
    PORT = 8080

    # Define a lambda function to clear the console based on the operating system
    clear = lambda: os.system("clear") if os.name == "posix" else os.system("cls")
    
    # Clear the console before running the Flask app
    clear()

    # Check if the data directory exists, if not, create it
    if not os.path.exists("./data"):
        os.mkdir("./data")

    # Run the Flask app with the specified host, port, and debug mode enabled
    app.run(host=HOST, port=PORT, debug=True)
