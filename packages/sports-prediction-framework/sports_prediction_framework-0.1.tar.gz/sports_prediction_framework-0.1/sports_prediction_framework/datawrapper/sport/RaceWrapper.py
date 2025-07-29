from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.datawrapper.DataHandler import DataHandler
class RaceWrapper(DataWrapper):

    name_columns = ['Player']
    name_id_columns = ['PID']
    rank_column = ['Rank']

    def __init__(self, data_handler: DataHandler, home_advantage):
        super().__init__(data_handler, home_advantage)