from flask import request
from server.statistics.devices import Devices
from pymongo.collection import ReturnDocument
from server.statistics.graphdata import GraphData
from server.config.source import ServerConfig, dbcursor


class Statistics(GraphData):
  def __init__(self):
    self.initdb = dbcursor.get_collection(ServerConfig.today)

  @property
  def viewers(self):
    return len(Devices().getwatchingdevices())

  @property
  def liked(self):
    return request.args.get("deviceId") in self.initdb.find_one({"streaming": True}).get("likes")

  def addlike(self):
    _return = ReturnDocument.AFTER
    device = request.args.get("deviceId")
    oldlikes = self.initdb.find_one({"streaming": True})
    if not device in oldlikes.get("likes"):
      data = self.initdb.find_one_and_update({"streaming": True}, {"$push": {"likes": device}}, return_document=_return)
      return {"likes": len(data.get("likes"))}
    return {"likes": len(oldlikes.get("likes"))}

  def getadminstats(self):
    stats = self.getstreamingdata()
    stats["devicecount"] = len(Devices().getconnecteddevices())
    return {**stats, **self.getweeklydata()}

  def getstreamingdata(self):
    _likes = []
    _comments = []
    for data in list(self.initdb.find()):
      if not data.get("streaming") == True:
        _user = dbcursor.users.find_one({"username": data.get("username")})
        if _user:
          _comments.append({"name": _user.get("name"), "comment": data.get("comment")})
      else:
        _likes = data.get("likes")
    return {"liked": self.liked, "likes": len(_likes), "comments": len(_comments), "comments_history": _comments}

  def addComment(self, comment):
    commentscount = self.initdb.count_documents({})
    print(f"{comment.get('username')} has posted a comment.")
    name = dbcursor.users.find_one({"username": comment.get("username")})
    self.initdb.insert_one({"username": name.get("username"), "comment": comment.get("comment")})
    return {"name": name.get("name"), "comment": comment.get("comment"), "comments": commentscount}

  def getgraphdata(self, timeframe):
    if timeframe == "Week":
      graphdata = self.getweeklydata()
    elif timeframe == "Month":
      graphdata = self.getmonthlydata()
    else:
      graphdata = self.getyearlydata()
    return graphdata
