from uuid import uuid4
from server.config.source import dbcursor
from server.security.security import SmartPaySecurity


class SmartPayAccount:
    def __init__(self, user: dict):
        self.user = user

    @property
    def genaccountnumber(self):
        number = 0
        for letter in self.user["fullname"]:
            number += int(ord(letter) & 31)
        gen_count = 15 - len(str(number))
        account = str(uuid4().int)[:gen_count]
        return f"3{number}{account}"

    @property
    def createaccount(self):
        self.user["balance"] = 0
        self.user["code"] = str(uuid4().int)[:6]
        self.user["accountnumber"] = self.genaccountnumber
        self.user["apikey"] = SmartPaySecurity.create_encryption_key()
        self.user['password'] = SmartPaySecurity(self.user).encrypt(self.user['password'])
        return self.user

    @property
    def currentaccount(self):
        return dbcursor.accounts.find_one({"username": self.user["username"]}, {"_id": 0})
