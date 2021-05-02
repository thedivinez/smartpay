from flask import request
from server.auth.processor import Auth
from flask_socketio import Namespace, emit
from server.statistics.processor import Statistics


class APISocket(Namespace):
  def on_connect(self):
    emit("connect", True, room=request.sid)

  def on_signup(self, account):
    emit("signup", Auth.signup(account), room=request.sid)

  def on_signin(self, account):
    emit("signin", Auth.signin(account), room=request.sid)

  def on_verifycode(self, account):
    emit("verifycode", Auth.verifycode(account), room=request.sid)

  def on_resendcode(self, account):
    emit("resendcode", Auth.sendcode(account), room=request.sid)

  def on_updateuser(self, userdata):
    emit("updateuser", Auth.updateuser(userdata), room=request.sid)

  def on_disconnect(self):
    emit("statistics", Statistics.disconnect_app(request.sid))