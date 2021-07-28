from flask import request
from flask_socketio import Namespace, emit
from server.auth.processor import SmartPayAuth
from server.statistics.devices import SystemUsers
from server.engine.transactions import SmartPayTransactions


class SmartPay(Namespace):

    # ================================================ Connect User =================================================

    def on_connect(self):
        emit("statistics", SystemUsers(request.args).connectuser)

    # ================================================ Authentication ===============================================

    def on_signup(self, account):
        emit("signup", SmartPayAuth({**account, **request.args}).signup, room=request.sid)

    def on_signin(self, account):
        emit("signin", SmartPayAuth({**account, **request.args}).signin, room=request.sid)

    def on_resendcode(self, account):
        emit("resendcode", SmartPayAuth({**account, **request.args}).sendcode(), room=request.sid)

    def on_verifycode(self, account):
        emit("verifycode", SmartPayAuth({**account, **request.args}).verifycode, room=request.sid)

    def on_updateuser(self, account):
        emit("updateuser", SmartPayAuth({**account, **request.args}).updateuser, room=request.sid)

    # ================================================ Transactions =================================================

    def on_deposit(self, account):
        emit("deposit", SmartPayTransactions({**account, **request.args}).deposit)

    def on_withdraw(self, account):
        emit("withdraw", SmartPayTransactions({**account, **request.args}).withdraw)

    def on_transferfunds(self, account):
        emit("transferfunds", SmartPayTransactions({**account, **request.args}).transferfunds)

    # ================================================ Disconnect User ==============================================

    def on_disconnect(self):
        emit("statistics", SystemUsers(request.args).disconnectuser)
