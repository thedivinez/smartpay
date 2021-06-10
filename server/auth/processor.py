from server.config.source import dbcursor
from server.security.security import Security
from pymongo.collection import ReturnDocument
from server.accounts.accounts import SmartPayAccount


class Auth:
  def __init__(self, user: dict) -> None:
    self.user = user

  def getuser(filter: dict):
    return dbcursor.users.find_one(filter, {"_id": 0})

  def signup(self):
    if Auth.getuser({"email": self.user.get("email")}):
      return {"status": "error", "message": "Email already in use."}
    self.user = SmartPayAccount(self.user).account
    if dbcursor.users.insert_one(self.user):
      return Auth.sendcode("Account created please enter OTP to continue.")
    return {"status": "error", "message": "Failed to create user."}

  def sendcode(self, message=None):
    user = Auth.getuser({"email": self.user.get("email")})
    print(self.user.get("code"))
    return {"status": "success", "message": message if message else "Code sent."}

  def verifycode(user: dict):
    if Auth.updateuser(user):
      return {"status": "success", "message": "You have successfully registered."}

  def updateuser(values: dict):
    _doc = ReturnDocument.AFTER
    _filter = {"apikey": values.get("apikey")}
    return dbcursor.users.find_one_and_update(_filter, values, projection={'_id': 0}, return_document=_doc)

  def signin(user: dict):
    existing = Auth.getuser({"email": user.get("email")})
    if existing:
      data = {"stored_pass": existing["password"], "input_pass": user.get("password")}
      if Security(data).veryfypassword():
        del existing['password']
        return {"status": "success", "account": existing}
    return {"status": "error", "message": "Invalid login credentials."}