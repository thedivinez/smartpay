from server.engine.accounts import SmartPayAccount
from server.config.source import dbcursor, ServerConfig


class SmartPayTransactions:
    def __init__(self, data: dict):
        self.data = data
        self.username = data["username"]
        self.amount = float(data["amount"])
        self.date = ServerConfig("datetime").today

    def addtosmartpayaccount(self, charges):
        dbcursor.accounts.update_one({"accountnumber": "smartpay01"}, {"$inc": {"balance": charges}})

    def calculatecharges(self, transaction, amount):
        return dbcursor.accounts.find_one({"accountnumber": "smartpay01"}, {transaction: 1})[transaction] * amount

    def recordtransaction(self, transaction):
        dbcursor.get_collection(ServerConfig().today).insert_one({**transaction, **{"date": self.date, "creator": self.username}})

    @property
    def withdraw(self):
        charges = self.calculatecharges("withdrawal", self.amount)
        balance = SmartPayAccount(self.data).currentaccount["balance"]
        if balance >= self.amount + charges:
            self.addtosmartpayaccount(charges)
            newbalance = balance - self.amount - charges
            print(f"{self.username} withdrew {self.amount}")
            self.recordtransaction({"type": "withdrawal", "amount": self.amount})
            dbcursor.accounts.update_one({"username": self.username}, {'$set': {'balance': newbalance}})
            return {"status": "success", "message": "The withdraw was successfull. Your new balance is $%f" % newbalance}
        return {"status": "error", "message": "Withdrawal amount exceeds current balance. Your current account balance is $%f" % balance}

    @property
    def transferfunds(self):
        charges = self.calculatecharges("transfer", self.amount)
        balance = SmartPayAccount(self.data).currentaccount["balance"]
        if SmartPayAccount({"username": self.data['recipient']}).findaccount:
            if balance >= self.amount + charges:
                self.addtosmartpayaccount(charges)
                newbalance = balance - self.amount - charges
                print(f"{self.username} transfered {self.amount} to {self.data['recipient']}")
                dbcursor.accounts.update_one({"username": self.username}, {'$set': {'balance': newbalance}})
                dbcursor.accounts.update_one({"username": self.data["recipient"]}, {"$inc": {"balance": self.amount}})
                self.recordtransaction({"type": "transfer", "amount": self.amount, "recipient": self.data["recipient"]})
                return {"status": "success", "message": f"${self.amount} transfer was successfull. Your new balance is ${newbalance}"}
            return {"status": "error", "message": f"Transfer amount exceeds current balance. Your current account balance is ${balance}"}
        return {"status": "error", "message": "Transfer failed account does not exist please make sure you have the correct username of the recipient."}

    @property
    def deposit(self):
        self.recordtransaction({"type": "deposit", "amount": self.amount})
        newbalance = SmartPayAccount(self.data).currentaccount["balance"] + self.amount
        dbcursor.accounts.update_one({"username": self.username}, {"$set": {"balance": newbalance}})
        return {"status": "success", "balance": newbalance, "message": "Deposit is successful and the balance in the account is $%f" % newbalance}