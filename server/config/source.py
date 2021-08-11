import pymongo
from flask import Flask
from pytz import timezone
from datetime import datetime
from flask_socketio import SocketIO

CONNECTION_STRING = "mongodb+srv://divine01:imwinning@splitcluster.aui7k.azure.mongodb.net/thedivinez?retryWrites=true&w=majority"
app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
dbcursor = pymongo.MongoClient(CONNECTION_STRING).smartpay


class ServerConfig:
    def __init__(self, action=None) -> None:
        self.action = action

    @property
    def today(self) -> str:
        now_africa = datetime.now(timezone("UTC")).astimezone(timezone("Africa/Harare"))
        return now_africa.strftime("%m-%d-%Y %H:%M:%S" if self.action == "datetime" else "%m-%d-%Y")
