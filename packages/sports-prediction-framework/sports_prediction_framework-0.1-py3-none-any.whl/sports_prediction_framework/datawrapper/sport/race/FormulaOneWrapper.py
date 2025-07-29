from sports_prediction_framework.datawrapper.sport.RaceWrapper import RaceWrapper


class FormulaOneWrapper(RaceWrapper):

    name = "Formula_One"

    def __init__(self,data_handler=None):
        super().__init__(data_handler, home_advantage=True)