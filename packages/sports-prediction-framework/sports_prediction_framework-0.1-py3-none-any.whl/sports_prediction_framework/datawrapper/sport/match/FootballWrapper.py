from sports_prediction_framework.datawrapper.sport.MatchWrapper import MatchWrapper
from sports_prediction_framework.datawrapper.sport.LeagueWrapper import LeagueWrapper


class FootballWrapper(MatchWrapper, LeagueWrapper):
    name = "Football"

    def __init__(self,data_handler=None):
        super().__init__(data_handler, home_advantage=True)