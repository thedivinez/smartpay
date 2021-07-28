from server.engine.accounts import SmartPayAccount
from server.config.source import dbcursor, ServerConfig


class SmartPayTransactions:
    def __init__(self, data: dict):
        self.data = data
        self.username = data["username"]
        self.date = ServerConfig("datetime").today
        self.data["amount"] = float(data["amount"])

    def addtosmartpayaccount(self, amount):
        dbcursor.accounts.update_one({"accountnumber": "smartpay01"}, {"$inc": {"balance": amount}})

    def calculatecharges(self, transaction, amount):
        return dbcursor.accounts.find_one({"accountnumber": "smartpay01"}, {transaction: 1})[transaction] * amount

    def recordtransaction(self, transaction):
        dbcursor.get_collection(self.date).insert_one({**transaction, **{"date": self.date, "creator": self.username}})

    @property
    def deposit(self):
        self.recordtransaction({"type": "deposit", "amount": self.data["amount"]})
        newbalance = SmartPayAccount(self.data).currentaccount["balance"] + self.data["amount"]
        dbcursor.accounts.update_one({"username": self.username}, {'$set': {'balance': newbalance}})
        return {"status": "success", "message": "Deposit is successful and the balance in the account is $%f" % newbalance}

    @property
    def withdraw(self):
        balance = SmartPayAccount(self.data).currentaccount["balance"]
        charges = self.calculatecharges("withdrawal", self.data["amount"])
        if balance >= self.data["amount"] + charges:
            self.addtosmartpayaccount(charges)
            newbalance = balance - self.data["amount"] - charges
            self.recordtransaction({"type": "withdrawal", "amount": self.data["amount"]})
            dbcursor.accounts.update_one({"username": self.username}, {'$set': {'balance': newbalance}})
            return {"status": "success", "message": "The withdraw was successfull. Your new balance is $%f" % newbalance}
        return {"status": "success", "message": "Withdrawal amount exceeds current balance. Your current account balance is $%f" % balance}

    @property
    def transferfunds(self):
        balance = SmartPayAccount(self.data).currentaccount["balance"]
        charges = self.calculatecharges("transfer", self.data["amount"])
        if balance >= self.data["amount"] + charges:
            self.addtosmartpayaccount(charges)
            newbalance = balance - self.data["amount"] - charges
            dbcursor.accounts.update_one({"username": self.username}, {'$set': {'balance': newbalance}})
            dbcursor.accounts.update_one({"username": self.data["recipient"]}, {'$inc': {'balance': self.data["amount"]}})
            self.recordtransaction({"type": "transfer", "amount": self.data["amount"], "recipient": self.data["recipient"]})
            return {"status": "success", "message": "Transfer successfull. Your new balance is $%f" % newbalance}
        return {"status": "success", "message": "Transfer amount exceeds current balance. Your current account balance is $%f" % balance}