from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.datawrapper.DataHandler import DataHandler


class MatchWrapper(DataWrapper):

    name_columns = ['Home','Away']
    name_id_columns = ['HID', 'AID']
    score_columns = ['HS', 'AS']
    result_column = ['WDL']
    prediction_columns = [1, 0, 2]

    def __init__(self, data_handler: DataHandler, home_advantage):
        super().__init__(data_handler, home_advantage)
        self.total_set_of_teams = self.get_set_of_teams()
        self.total_number_of_teams = len(self.total_set_of_teams)
        self.total_set_of_teams_ids = set()

    def set_after_compute_values(self):
        self.total_set_of_teams = self.get_set_of_teams()
        self.total_number_of_teams = len(self.total_set_of_teams)

    def get_set_of_teams(self):
        return set(self.data_handler.dataframe['Home']).union(set(self.data_handler.dataframe['Away']))

    def get_set_of_teams_ids(self):
        return set(self.data_handler.dataframe['HID']).union(set(self.data_handler.dataframe['AID']))

    def get_labels(self):
        return self.get_dataframe()['WDL']