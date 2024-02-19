from src import password_generator
import argon2, hashlib

# Initialise the password generator
generator = password_generator.Generator()
hasher = argon2.PasswordHasher()


class Credential:
    def __init__(self, username, password, email=None, website=None, notes=None):
        self.username = username
        self.password = password
        self.email = email
        self.website = website
        self.notes = notes

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

    def add_cred(
        self,
        username,
        password=generator.generate(8, 1),
        email=None,
        website=None,
        notes=None,
    ):
        self.__creds.append(Credential(username, password, email, website, notes))

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
        return creds
