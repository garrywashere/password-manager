class Login:
    def __init__(self, username, password, email=None, website=None, notes=None):
        self.username = username
        self.password = password
        self.email = email
        self.website = website
        self.notes = notes


class User:
    def __init__(self, username, master_password):
        self.username = username
        self.__password = master_password
        self.__logins = []

    def validate_password(self, password):
        if password == self.__password:
            return True
        else:
            return False

    def add_login(self, username, password, email=None, website=None, notes=None):
        self.__logins.append(Login(username, password, email, website, notes))

    def query_login(self, query):
        for login in self.__logins:
            if (
                query in login.username
                or query in login.email
                or query in login.website
            ):
                return login