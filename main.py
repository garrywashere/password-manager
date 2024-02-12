from InquirerPy import inquirer as inq
from InquirerPy.separator import Separator
from src import frontend
import os

clear = lambda: os.system("clear") if os.name == "posix" else os.system("cls")

def main():
    running = True
    while running:
        clear()
        print("Welcome to Password Manager.\n")
        choices = ["Start server", Separator(), "Exit"]
        choice = inq.select(message="Make a selection", choices=choices).execute()
        match choice:
            case "Start server":
                frontend.app.run(host="127.0.0.1", port=8080, debug=True)
            case "Exit":
                running = False
                exit()

if __name__ == "__main__":
    try:
        main()
    # except Exception as e:
    #     print("Error:", e)
    except KeyboardInterrupt:
        print("Exiting")
        exit()