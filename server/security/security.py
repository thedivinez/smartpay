from cryptography.fernet import Fernet


class SmartPaySecurity:
  def __init__(self, data: dict) -> None:
    self.data = data
    self.apikey = data.get("apikey")

  @staticmethod
  def create_encryption_key() -> str:
    return Fernet.generate_key().decode()

  @property
  def encryptionkey(self):
    return Fernet(self.apikey)

  def encryptdict(self):
    for key, value in self.data.items():
      self.data[key] = self.encrypt(value)
    return self.data

  def veryfypassword(self) -> bool:
    return self.decrypt(self.data["stored_pass"]) == self.data["input_pass"]

  def encrypt(self, custom_txt) -> bytes:
    return self.encryptionkey.encrypt(str(custom_txt if custom_txt else self.data["message"]).encode())

  def decrypt(self, stored_pass=None) -> str:
    return self.encryptionkey.decrypt(str(stored_pass if stored_pass else self.data["message"]).encode()).decode()