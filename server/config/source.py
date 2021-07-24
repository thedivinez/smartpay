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
    def __init__(self, action=None) -> None:
        self.action = action

    @property
    def today(self) -> str:
        now_africa = datetime.now(timezone("UTC")).astimezone(timezone("Africa/Harare"))
        return now_africa.strftime("%m-%d-%Y %H:%M:%S" if self.action == "datetime" else "%m-%d-%Y")
