from uuid import uuid4
from server.security.config import dbcursor
from server.security.security import Security
from pymongo.collection import ReturnDocument


class Auth:
  def signup(user: dict):
    if Auth.getuser({"email": user.get("email")}):
      return {"status": "error", "message": "Email already in use."}
    user["code"] = str(uuid4().int)[:6]
    user["apikey"] = Security.create_encryption_key()
    user['password'] = Security(user).encrypt(user.get('password'))
    if dbcursor.users.insert_one(user):
      return Auth.sendcode(user, "Account created please enter OTP to continue.")
    return {"status": "error", "message": "Failed to create user."}

  def getuser(filter: dict):
    return dbcursor.users.find_one(filter, {"_id": 0})

  def verifycode(user: dict):
    if Auth.updateuser(user):
      return {"status": "success", "message": "You have successfully registered."}

  def updateuser(values: dict):
    _doc = ReturnDocument.AFTER
    _filter = {"apikey": values.get("apikey")}
    return dbcursor.users.find_one_and_update(_filter, values, projection={'_id': 0}, return_document=_doc)

  def sendcode(user: dict, message=None):
    user = Auth.getuser({"email": user.get("email")})
    print(user.get("code"))
    return {"status": "success", "message": message if message else "Code sent."}

  def signin(user: dict):
    existing = Auth.getuser({"email": user.get("email")})
    if existing:
      data = {"stored_pass": existing["password"], "input_pass": user.get("password")}
      if Security(data).veryfypassword():
        del existing['password']
        return {"status": "success", "account": existing}
    return {"status": "error", "message": "Invalid login credentials."}