from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.datawrapper.DataHandler import DataHandler
import pandas as pd


class LeagueWrapper(DataWrapper):

    league_column = 'League'

    def __init__(self, data_handler: DataHandler, home_advantage):
        super().__init__(data_handler, home_advantage)
        self.number_of_teams_by_leagues = {}
        self.total_number_of_leagues = 0

    def set_after_compute_values(self):
        self.number_of_teams_by_leagues = self.get_number_of_teams_by_league()
        self.total_number_of_leagues = len(self.get_leagues())

    def get_leagues(self):
        return pd.unique(self.get_dataframe()[self.league_column])

    def get_number_of_teams_by_league(self):
        dict = {}
        for league,group_values in self.get_dataframe().groupby([self.league_column]):
            dict[league] = len(set(group_values['Home']).union(set(group_values['Away'])))
        return dict

"""    @staticmethod
    def league_scope(wrapper:LeagueWrapper):
        return EnumSelector(EnumScope(wrapper.get_leagues(), wrapper.league_column))"""

