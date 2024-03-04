import argon2, hashlib

hasher = argon2.PasswordHasher()


class Credential:
    def __init__(
        self, username, password, email=None, website=None, notes=None, views=0
    ):
        self.username = username
        self.password = password
        self.email = email
        self.website = website
        self.notes = notes

        self.views = views

        hash = hashlib.md5()
        hash.update(username.encode() + password.encode())
        self.id = hash.hexdigest()


class User:
    def __init__(self, username, master_password):
        self.username = username
        self.__password = hasher.hash(master_password)
        self.__creds = []

    def verify_password(self, password):
        try:
            if hasher.verify(self.__password, password):
                return True
        except argon2.exceptions.VerifyMismatchError:
            return False

    def change_password(self, newPassword):
        self.__password = hasher.hash(newPassword)

    def add_cred(
        self,
        username,
        password,
        email=None,
        website=None,
        notes=None,
        views=0,
    ):
        self.__creds.append(
            Credential(username, password, email, website, notes, views)
        )

    def list_creds(self):
        return [cred for cred in self.__creds]

    def del_cred(self, id):
        for cred in self.__creds:
            if cred.id == id:
                self.__creds.remove(cred)

    def query(self, query):
        creds = []
        for cred in self.__creds:
            if query in cred.username or query in cred.email or query in cred.website:
                creds.append(cred)
        if not creds:
            creds = "404"
        return creds
