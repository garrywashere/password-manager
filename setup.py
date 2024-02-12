import subprocess, sys

def setup():
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    subprocess.run(["venv/bin/pip", "install", "--upgrade", "pip"])
    subprocess.run(["venv/bin/pip", "install", "-r", "requirements.txt"])

if __name__ == "__main__":
    setup()