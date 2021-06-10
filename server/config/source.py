import pymongo
from flask import Flask
from pytz import timezone
from datetime import datetime
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)
dbcursor = pymongo.MongoClient().smartpay
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False


class ServerConfig:
  @property
  def today():
    now_utc = datetime.now(timezone("UTC"))
    now_africa = now_utc.astimezone(timezone("Africa/Harare"))
    return now_africa.strftime("%m-%d-%Y %H:%M:%S")

  @property
  def prepareserver():
    return