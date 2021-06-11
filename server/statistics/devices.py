from flask import request
from server.config.source import dbcursor
from server.config.source import ServerConfig


class Devices:
  def __init__(self):
    self.device = request.args.get("deviceId")
    self.initdb = dbcursor.get_collection(ServerConfig.today)

  def connectdevice(self):
    "sets device online status to True."
    ServerConfig.prepareserver  # === create collection if not exists ===
    _filter = {"type": "diviceactivity", "devices.deviceid": self.device}
    if not self.device == "admin":
      if not self.initdb.find_one(_filter):
        device = {"deviceid": self.device, "online": True}
        self.initdb.update_one({"type": "diviceactivity"}, {"$push": {"devices": device}})
      else:
        self.initdb.update_one(_filter, {"$set": {"devices.$.online": True}})
    print(f"{self.device} has connected.")

  def disconnectdevice(self):
    "sets device online status to False."
    if not self.device == "admin":
      _filter = {"type": "diviceactivity", "devices.deviceid": self.device}
      self.initdb.update_one(_filter, {"$set": {"devices.$.online": False}})
    print(f"{self.device} disconnected.")

  def getdeviceshistory(self):
    "returns a list of devices that came online that day."
    return self.initdb.find_one({"type": "diviceactivity"}).get("devices")

  def getconnecteddevices(self):
    "returns a list of connected devices"
    _cond = [{"$ifNull": ["$online", True]}, True]
    redact = {"$redact": {"$cond": [{"$eq": _cond}, "$$DESCEND", "$$PRUNE"]}}
    devices = list(self.initdb.aggregate([{"$match": {"devices.online": True}}, redact]))
    return devices[0].get("devices") if devices else []