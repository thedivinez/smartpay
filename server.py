from server.apisocket import SmartPay
from server.config.source import app, socketio

socketio.on_namespace(SmartPay("/smartpay"))

if __name__ == "__main__":
  socketio.run(app, debug=True, host="0.0.0.0")