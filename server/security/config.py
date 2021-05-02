import pymongo
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)
dbcursor = pymongo.MongoClient().smartpay
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False