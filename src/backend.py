from src import password_generator

# Initialize the password generator
generator = password_generator.Generator()


class Login:
    def __init__(self, username, password, email=None, website=None, notes=None):
        """
        Initialize a Login instance.

        Parameters:
        - username (str): The username for the login.
        - password (str): The password for the login.
        - email (str): Optional email associated with the login.
        - website (str): Optional website associated with the login.
        - notes (str): Optional notes for the login.
        """
        self.username = username
        self.password = password
        self.email = email
        self.website = website
        self.notes = notes


class User:
    def __init__(self, username, master_password):
        """
        Initialize a User instance.

        Parameters:
        - username (str): The username for the user.
        - master_password (str): The master password for the user.
        """
        self.username = username
        self.__password = master_password
        self.__logins = []  # List to store login information

    def validate_password(self, password):
        """
        Validate the user's password.

        Parameters:
        - password (str): The password to be validated.

        Returns:
        - bool: True if the password is valid, False otherwise.
        """
        return password == self.__password

    def add_login(
        self,
        username,
        password=generator.generate(8, 1),
        email=None,
        website=None,
        notes=None,
    ):
        """
        Add a new login to the user's logins list.

        Parameters:
        - username (str): The username for the login.
        - password (str): The password for the login. If not provided, a generated password is used.
        - email (str): Optional email associated with the login.
        - website (str): Optional website associated with the login.
        - notes (str): Optional notes for the login.
        """
        self.__logins.append(Login(username, password, email, website, notes))

    def query_login(self, query):
        """
        Query the user's logins based on a search query.

        Parameters:
        - query (str): The search query.

        Returns:
        - Login or None: The matching login or None if no match is found.
        """
        for login in self.__logins:
            if (
                query in login.username
                or query in login.email
                or query in login.website
            ):
                return login
        return None

    def list_logins(self):
        """
        List all logins associated with the user.

        Returns:
        - dict: A dictionary where keys are usernames and values are lists containing email and website information.
        """
        logins = {}
        for login in self.__logins:
            logins[login.username] = [login.email, login.website]
        return logins
