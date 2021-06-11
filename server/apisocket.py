from flask import request
from flask_socketio import Namespace, emit
from server.statistics.devices import Devices
from server.auth.processor import SmartPayAuth


class SmartPay(Namespace):
  def on_connect(self):
    emit("statistics", Devices().connectdevice())

  def on_signup(self, account):
    emit("signup", SmartPayAuth.signup(account), room=request.sid)

  def on_signin(self, account):
    emit("signin", SmartPayAuth.signin(account), room=request.sid)

  def on_resendcode(self, account):
    emit("resendcode", SmartPayAuth.sendcode(account), room=request.sid)

  def on_verifycode(self, account):
    emit("verifycode", SmartPayAuth.verifycode(account), room=request.sid)

  def on_updateuser(self, userdata):
    emit("updateuser", SmartPayAuth.updateuser(userdata), room=request.sid)

  def on_disconnect(self):
    emit("statistics", Devices().disconnectdevice())