from server.config.source import dbcursor
from server.config.source import ServerConfig


class SystemUsers(object):
    def __init__(self, data: dict):
        self.user = data.get("username")
        self.date = ServerConfig().today
        self.initdb = dbcursor.get_collection("useractivity")

    def prepareuseractivity(self):
        if not self.initdb.find_one({"date": self.date}):
            self.initdb.insert_one({"date": self.date, "users": []})

    def getusershistory(self):
        "returns a list of users that came online that day."
        return self.initdb.find_one({"date": self.date}).get("users")

    @property
    def connectuser(self):
        "set online status true"
        self.prepareuseractivity()
        sfilter = {"date": self.date, "users.username": self.user}
        if self.user and not self.user == "admin":
            if self.initdb.find_one(sfilter):
                self.initdb.update_one(sfilter, {"$set": {"users.$.online": True}})
            else:
                user = {"username": self.user, "online": True}
                self.initdb.update_one({"date": self.date}, {"$push": {"users": user}})
        print(f"=== {self.user} has connected.")
        return self.getconnectedusers

    @property
    def getconnectedusers(self):
        "returns a list of connected users"
        _cond = [{"$ifNull": ["$online", True]}, True]
        redact = {"$redact": {"$cond": [{"$eq": _cond}, "$$DESCEND", "$$PRUNE"]}}
        users = list(self.initdb.aggregate([{"$match": {"users.online": True}}, redact]))
        return users[0].get("users") if users else []

    @property
    def disconnectuser(self):
        "sets online status false"
        if not self.user == "admin":
            self.initdb.update_one({"date": self.date, "users.username": self.user}, {"$set": {"users.$.online": False}})
        print(f"=== {self.user} disconnected.")
        return self.getconnectedusers