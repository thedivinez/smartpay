from server.statistics.graphdata import GraphData
from server.config.source import ServerConfig, dbcursor


class Statistics(GraphData):
    def __init__(self):
        self.initdb = dbcursor.get_collection(ServerConfig.today)

    def getgraphdata(self, timeframe):
        if timeframe == "Week":
            graphdata = self.getweeklydata()
        elif timeframe == "Month":
            graphdata = self.getmonthlydata()
        else:
            graphdata = self.getyearlydata()
        return graphdata
