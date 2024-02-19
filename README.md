# Password Manager Project

![WakaTime](https://wakatime.com/badge/user/018d88ca-6686-4ddc-a648-a108b3febbc3/project/018d8f86-dd38-4eca-93ef-598d3d05e6aa.svg)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/garrywashere/password-manager)

## Overview

This Python-based Password Manager is designed as part of the OCR Computer Science H446 programming project. The goal of this project is to create a secure and user-friendly password manager to help users manage their passwords effectively.

![Index](screenshots/index.png)

## Features

- **User Authentication:** Allows users to create an account with a unique username and a secure password.
- **Password Storage:** Safely stores and encrypts user passwords.
- **Password Generation:** Provides a tool to generate strong, random passwords.
- **Data Security:** Implements secure practices for storing and handling sensitive information.
- **User Interface:** A simple and intuitive web interface for user interaction.
- **Local Storage:** Provides peace of mind when data is stored locally completely under the users control.

## Requirements
- Python (3.10 or above)
- requirements.txt (see Installation step 5)
- Web Browser

That's it


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/garrywashere/password-manager.git
   ```

2. Navigate to the project directory:

   ```bash
   cd password-manager
   ```

3. Initiate the virtual environment:

   ```bash
   python -m venv venv
   ```

4. Enter the virtual envrionment

   ```bash
   source venv/bin/activate
   ```

5. Install required libraries from requirements.txt

   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage

1. Run the server

```bash
python main.py
```

NOTE: to change server settings modify the constants in the `main.py` script:
```python
HOST = "127.0.0.1"
PORT = 8080
```

2. Navigate to `https://127.0.0.1:8080/`