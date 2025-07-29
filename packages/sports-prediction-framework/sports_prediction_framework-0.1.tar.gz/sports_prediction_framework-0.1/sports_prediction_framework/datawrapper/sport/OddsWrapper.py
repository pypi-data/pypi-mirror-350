from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.datawrapper.DataHandler import DataHandler
class OddsWrapper(DataWrapper):

    name = "Odds"
    name_columns = ['Bookmaker', 'Timestamp', '1', 'X', '2']
    name_id_columns = ['MatchID']

    def __init__(self, data_handler: DataHandler):
        super().__init__(data_handler=data_handler, home_advantage=True)