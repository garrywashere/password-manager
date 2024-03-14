import argon2  # Importing argon2 for password hashing
import hashlib  # Importing hashlib for hashing
import pyotp  # Importing pyotp for TOTP (Time-Based One-Time Password) generation
import os  # Importing os for miscellaneous operating system interfaces

hasher = argon2.PasswordHasher()  # Creating a PasswordHasher object for hashing passwords


class Credential:
    def __init__(
        self, username, password, email=None, website=None, notes=None, views=0
    ):
        """
        Initialize a Credential object.

        Parameters:
        - username (str): The username associated with the credential.
        - password (str): The password associated with the credential.
        - email (str, optional): The email associated with the credential. Default is None.
        - website (str, optional): The website associated with the credential. Default is None.
        - notes (str, optional): Additional notes associated with the credential. Default is None.
        - views (int, optional): Number of views for the credential. Default is 0.
        """
        self.username = username
        self.password = password
        self.email = email
        self.website = website
        self.notes = notes
        self.views = views

        # Generating a unique ID for the credential based on username and password
        hash = hashlib.md5()
        hash.update(username.encode() + password.encode())
        self.id = hash.hexdigest()


class User:
    def __init__(self, username, master_password):
        """
        Initialize a User object.

        Parameters:
        - username (str): The username of the user.
        - master_password (str): The master password used for authentication.
        """
        self.username = username
        # Hashing the master password for secure storage
        self.__password = hasher.hash(master_password)
        # Generating a random base32 key for TOTP (Time-Based One-Time Password) authentication
        self.__totp_key = pyotp.random_base32()
        self.__creds = []  # List to store user's credentials

    def verify_password(self, password):
        """
        Verify if the provided password matches the user's master password.

        Parameters:
        - password (str): The password to be verified.

        Returns:
        - bool: True if the password matches, False otherwise.
        """
        try:
            if hasher.verify(self.__password, password):
                return True
        except argon2.exceptions.VerifyMismatchError:
            return False

    def change_password(self, newPassword):
        """
        Change the user's master password.

        Parameters:
        - newPassword (str): The new master password.
        """
        self.__password = hasher.hash(newPassword)

    def totp_get(self):
        """
        Get the TOTP provisioning URI.

        Returns:
        - str: The TOTP provisioning URI.
        """
        return pyotp.totp.TOTP(self.__totp_key).provisioning_uri(
            name=self.username, issuer_name="Password Manager"
        )

    def totp_verify(self, code):
        """
        Verify the provided TOTP code.

        Parameters:
        - code (str): The TOTP code to be verified.

        Returns:
        - bool: True if the code is valid, False otherwise.
        """
        totp = pyotp.TOTP(self.__totp_key)
        return totp.verify(code)

    def add_cred(
        self,
        username,
        password,
        email=None,
        website=None,
        notes=None,
        views=0,
    ):
        """
        Add a new credential to the user's list of credentials.

        Parameters:
        - username (str): The username associated with the credential.
        - password (str): The password associated with the credential.
        - email (str, optional): The email associated with the credential. Default is None.
        - website (str, optional): The website associated with the credential. Default is None.
        - notes (str, optional): Additional notes associated with the credential. Default is None.
        - views (int, optional): Number of views allowed for the credential. Default is 0.
        """
        self.__creds.append(
            Credential(username, password, email, website, notes, views)
        )

    def list_creds(self):
        """
        Get a list of all credentials associated with the user.

        Returns:
        - list: List of Credential objects.
        """
        return [cred for cred in self.__creds]

    def del_cred(self, id):
        """
        Delete a credential from the user's list of credentials.

        Parameters:
        - id (str): The unique ID of the credential to be deleted.
        """
        for cred in self.__creds:
            if cred.id == id:
                self.__creds.remove(cred)

    def query(self, query):
        """
        Search for credentials based on a query.

        Parameters:
        - query (str): The search query.

        Returns:
        - list: List of Credential objects matching the query.
        """
        creds = []
        for cred in self.__creds:
            if query in cred.username or query in cred.email or query in cred.website:
                creds.append(cred)
        if not creds:
            creds = "404"  # Return "404" if no credentials match the query
        return creds
