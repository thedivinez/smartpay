from server.accounts.accounts import SmartPayAccount
from server.config.source import dbcursor, ServerConfig


class SmartPayTransactions:
  def __init__(self, data: dict):
    self.data = data

  def recordtransaction(self, transaction):
    transaction["date"] = ServerConfig.today
    transaction["creator"] = self.data["username"]
    dbcursor.transactions.insert_one(transaction)

  def calculatecharges(self, transaction, amount):
    return dbcursor.configs.find_one({"type": "charges"}, {transaction: 1})[transaction] * amount

  def deposit(self):
    self.recordtransaction({"type": "deposit", "amount": self.data["amount"]})
    newbalance = SmartPayAccount(self.data).currentaccount["balance"] + self.data["amount"]
    dbcursor.accounts.update_one({"username": self.data["username"]}, {'$set': {'balance': newbalance}})
    return {"status": "success", "message": "Deposit is successful and the balance in the account is $%f" % newbalance}

  def withdraw(self):
    balance = SmartPayAccount(self.data).createaccount["balance"]
    if balance >= self.data["amount"]:
      self.recordtransaction({"type": "withdrawal", "amount": self.data["amount"]})
      newbalance = balance - self.calculatecharges("withdrawal", self.data["amount"])
      dbcursor.accounts.update_one({"username": self.data["username"]}, {'$set': {'balance': newbalance}})
      return {"status": "success", "message": "The withdraw is successfull. Your new balance is $%f" % newbalance}
    else:
      return {"status": "success", "message": "Insuficient Balance. Your current account balance is $%f" % balance}

  def transferfunds(self):
    balance = SmartPayAccount(self.data).createaccount["balance"]
    if balance >= self.data["amount"]:
      newbalance = balance - self.data["amount"]
      dbcursor.accounts.update_one({"username": self.data["username"]}, {'$set': {'balance': newbalance}})
      dbcursor.accounts.update_one({"username": self.data["recipient"]}, {'$inc': {'balance': self.data["amount"]}})
      self.recordtransaction({"type": "transfer", "amount": self.data["amount"], "recipient": self.data["recipient"]})
      return {"status": "success", "message": "Transfer successfull. Your new balance is $%f" % newbalance}
    else:
      return {"status": "success", "message": "Insuficient Balance. Your current account balance is $%f" % balance}