class SolvingAgent:
    def getAction(self, tileMatrix):
        raise NotImplementedError("getAction not implemented")


class ChallengingAgent:
    def getNewTile(self, tileMatrix):
        raise NotImplementedError("getNewTile not implemented")
