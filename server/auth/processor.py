from server.config.source import dbcursor
from pymongo.collection import ReturnDocument
from server.engine.accounts import SmartPayAccount
from server.security.security import SmartPaySecurity


class SmartPayAuth:
  def __init__(self, user: dict) -> None:
    self.user = user

  def getuser(self, filter: dict):
    return dbcursor.users.find_one(filter, {"_id": 0})

  def signup(self):
    if self.getuser({"email": self.user.get("email")}):
      return {"status": "error", "message": "Email already in use."}
    self.user = SmartPayAccount(self.user).createaccount
    if dbcursor.users.insert_one(self.user):
      return self.sendcode("Account created please enter OTP to continue.")
    return {"status": "error", "message": "Failed to create user."}

  def signin(user: dict):
    existing = SmartPayAuth.getuser({"email": user.get("email")})
    if existing:
      data = {}
      data["apikey"] = existing["apikey"]
      data["input_pass"] = user.get("password")
      data["stored_pass"] = existing["password"]
      if SmartPaySecurity(data).veryfypassword():
        del existing['password']
        return {"status": "success", "account": existing}
    return {"status": "error", "message": "Invalid login credentials."}

  def sendcode(self, message=None):
    user = self.getuser({"email": self.user.get("email")})
    print(self.user.get("code"))
    return {"status": "success", "message": message if message else "Code sent."}

  def verifycode(user: dict):
    if SmartPayAuth.updateuser(user):
      return {"status": "success", "message": "You have successfully registered."}

  def updateuser(values: dict):
    _doc = ReturnDocument.AFTER
    _filter = {"apikey": values.get("apikey")}
    return dbcursor.users.find_one_and_update(_filter, values, projection={'_id': 0}, return_document=_doc)