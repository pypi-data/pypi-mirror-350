from sports_prediction_framework.datawrapper.sport.RaceWrapper import RaceWrapper


class GolfWrapper(RaceWrapper):

    name = "Golf"

    def __init__(self,data_handler=None):
        super().__init__(data_handler, home_advantage=True)

