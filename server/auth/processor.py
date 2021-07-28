from server.config.source import dbcursor
from pymongo.collection import ReturnDocument
from server.engine.accounts import SmartPayAccount
from server.security.security import SmartPaySecurity


class SmartPayAuth:
    def __init__(self, user: dict) -> None:
        self.user = user

    def checknumber(self):
        return dbcursor.accounts.find_one({"phome": self.user.get("phone")}, {"_id": 0})

    def finduser(self):
        return dbcursor.accounts.find_one({"username": self.user.get("username")}, {"_id": 0})

    @property
    def signin(self):
        existing = self.finduser()
        if existing:
            data = {}
            data["apikey"] = existing.get("apikey")
            data["stored_pass"] = existing.get("password")
            data["input_pass"] = self.user.get("password")
            if SmartPaySecurity(data).veryfypassword():
                if existing.get("verified"):
                    del existing['code']
                    del existing['apikey']
                    del existing['verified']
                    del existing['password']
                    return {"status": "success", "account": existing}
                return self.sendcode("Account not verified please enter OTP to continue.")
        return {"status": "error", "message": "Invalid login credentials."}

    def sendcode(self, message=None):
        user = self.finduser()
        return {"status": "verifycode", "message": message if message else "Code sent."}

    @property
    def verifycode(self):
        if self.finduser().get("code") == self.user.get("code"):
            self.user["verified"] = True
            if self.updateuser.get("verified"):
                return {"status": "success", "message": "Account verified"}
        return {"status": "error", "message": "Invalid code"}

    @property
    def signup(self):
        if self.finduser():
            return {"status": "error", "message": "Username already in use."}
        if self.checknumber():
            return {"status": "error", "message": "The phone number is associated with another account please go to sign in if it's your account."}
        self.user = SmartPayAccount(self.user).createaccount
        if dbcursor.accounts.insert_one(self.user):
            return self.sendcode("Account created please enter OTP to continue.")
        return {"status": "error", "message": "Failed to create user."}

    @property
    def updateuser(self):
        _filter = {"username": self.user.get("username")}
        response = dbcursor.accounts.find_one_and_update(_filter, {"$set": self.user}, projection={'_id': 0}, return_document=ReturnDocument.AFTER)
        return response if response else {}