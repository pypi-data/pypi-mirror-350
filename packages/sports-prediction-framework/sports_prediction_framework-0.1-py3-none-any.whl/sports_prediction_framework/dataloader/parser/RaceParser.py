from sports_prediction_framework.dataloader.parser.AbstractParser import AbstractParser
import pandas as pd


class RaceParser(AbstractParser):
    def parse_flashscore(self, data: pd.DataFrame) -> pd.DataFrame:
        data = self.remove_not_valid_results(data)
        data = self.parse_score_PSQL(data)
        return data

    def parse_isdb(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def remove_not_valid_results(self, data: pd.DataFrame):
        return data[data["Rank"].notnull()]


    def parse_score_PSQL(self, data: pd.DataFrame):
        data['Rank'] = data['Rank'].str.replace('.', '')
        return data