from enum import Enum
from sports_prediction_framework.dataloader.parser.MatchParser import MatchParser
from sports_prediction_framework.datawrapper.sport.match import FootballWrapper, AmericanFootballWrapper,BaseballWrapper,BasketballWrapper, HockeyWrapper
from sports_prediction_framework.dataloader.parser.RaceParser import RaceParser
from sports_prediction_framework.datawrapper.sport.race import GolfWrapper, CyclingWrapper, FormulaOneWrapper


class SportType(Enum):
    FOOTBALL = (MatchParser, FootballWrapper)
    GOLF = (RaceParser, GolfWrapper)
    AMERICAN_FOOTBALL = (MatchParser, AmericanFootballWrapper)
    BASEBALL = (MatchParser, BaseballWrapper)
    BASKETBALL = (MatchParser, BasketballWrapper)
    HOCKEY = (MatchParser, HockeyWrapper)
    CYCLING = (RaceParser, CyclingWrapper)
    FORMULA_ONE = (RaceParser, FormulaOneWrapper)


    def get_parser(self):
        return self.value[0]

    def get_wrapper(self):
        return self.value[1]
