from paypalrestsdk import Payment, configure


def makepayment(payment_data: dict):
  configure({
      'mode': 'sandbox',  #sandbox or live
      'client_id': 'AeXYJ7z63_L9HPCe5-Oi5_YeXeosZQa0nhKjrU0RJERC0L7x4p-Gid9X08nY-E1z729sO4Dd8H_m2pun',
      'client_secret': 'EIYkEWVOCJjFt4RD1s1vo7r6kWe1-sqqU1ZuM8T095CbvhBI6dAioHraoRaGUHLElox5x20zkTwd8PhN'
  })
  payment_config = {}
  payment_config["intent"] = "sale"
  payment_config["payer"]["payment_method"] = "paypal"
  payment_config["transactions"]["amount"]["total"] = payment_data.get('amount')
  payment_config["transactions"]["description"] = payment_data.get('description')
  payment_config["transactions"]["amount"]["currency"] = payment_data.get('currency')
  payment_config["redirect_urls"]["cancel_url"] = "https://api.ministryofeducation.gov/paypal/cancel"
  payment_config["redirect_urls"]["return_url"] = "https://api.ministryofeducation.gov/paypal/process"
  payment = Payment(payment_config)
  return [link for link in payment.links if link.method == "REDIRECT"][0].href if payment.create() else payment.error
