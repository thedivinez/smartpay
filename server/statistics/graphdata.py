from pytz import timezone
from datetime import datetime, timedelta
from server.config.source import dbcursor
from server.statistics.devices import Devices
from server.config.source import ServerConfig


class GraphData:

  _data = {}

  @staticmethod
  def currentzimdate():
    now_utc = datetime.now(timezone('UTC'))
    return now_utc.astimezone(timezone('Africa/Harare'))

  @staticmethod
  def chunks(lst, n):
    for i in range(0, len(lst), n):
      yield lst[i:i + n]

  def getweeklydata(self):
    day = 7
    while day >= 0:
      data = dbcursor.get_collection(ServerConfig.today).find_one({"type": "diviceactivity"})
      if data:
        self._data[day] = {'devicecount': len(Devices().getconnecteddevices())}
      day -= 1
    return {"graphdata": self._data}

  def getmonthlydata(self):
    month = 0
    currentday = self.currentzimdate()
    currentyear = currentday.year
    while currentyear >= 2020:
      init = {'devicecount': 0}
      first = currentday.replace(day=1)
      _monthpref = first.strftime('%Y-%b-')
      lastmonth = first - timedelta(days=1)
      for collection in dbcursor.list_collection_names():
        if collection.startswith(f"streamed_{_monthpref}"):
          _data = dbcursor.get_collection(ServerConfig.today).find_one({"type": "diviceactivity"})
          if _data:
            devicecount = init["devicecount"] + _data["userscount"]
            init = {'devicecount': devicecount}
          self._data[month * 28] = init
      currentday = lastmonth.replace(day=28)
      currentyear = lastmonth.year
      month += 1
    return {"graphdata": self._data}

  def getyearlydata(self):
    __days = 0
    init = {'devicecount': 0}
    _monthlydata = self.getmonthlydata()["graphdata"]
    _chunks = list(self.chunks(list(_monthlydata.keys()), 12))
    for index, _chunk in enumerate(_chunks):
      for _month in _chunk:
        devicecount = init["devicecount"] + _monthlydata[_month]["devicecount"]
        init = {'devicecount': devicecount}
        __days += _month
      self._data[index * 364] = init
    return {"graphdata": self._data}
