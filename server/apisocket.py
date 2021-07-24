from flask import request
from flask_socketio import Namespace, emit
from server.auth.processor import SmartPayAuth
from server.statistics.devices import SystemUsers
from server.engine.transactions import SmartPayTransactions


class SmartPay(Namespace):

    # ============================== Connect User ===============================

    def on_connect(self):
        emit("statistics", SystemUsers(request.args).connectuser)

    # ============================== Authentication =============================

    def on_signup(self, account):
        emit("signup", SmartPayAuth(account).signup, room=request.sid)

    def on_signin(self, account):
        emit("signin", SmartPayAuth(account).signin, room=request.sid)

    def on_resendcode(self, account):
        emit("resendcode", SmartPayAuth(account).sendcode(), room=request.sid)

    def on_verifycode(self, account):
        emit("verifycode", SmartPayAuth(account).verifycode, room=request.sid)

    def on_updateuser(self, account):
        emit("updateuser", SmartPayAuth(account).updateuser, room=request.sid)

    # =============================== Transactions ==============================

    def on_deposit(self, data):
        emit("deposit", SmartPayTransactions(data).deposit)

    def on_withdraw(self, data):
        emit("withdraw", SmartPayTransactions(data).withdraw)

    def on_transferfunds(self, data):
        emit("transferfunds", SmartPayTransactions(data).transferfunds)

    # ============================== Disconnect User =============================

    def on_disconnect(self):
        emit("statistics", SystemUsers(request.args).disconnectuser)
