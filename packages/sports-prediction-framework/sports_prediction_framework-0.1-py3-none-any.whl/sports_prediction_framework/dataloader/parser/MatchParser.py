from sports_prediction_framework.dataloader.parser.AbstractParser import AbstractParser
import pandas as pd
import numpy as np


class MatchParser(AbstractParser):
    def parse_flashscore(self, data: pd.DataFrame) -> pd.DataFrame:
        data = self.remove_not_valid_results(data)
        data = self.parse_score_PSQL(data)
        data = self.parse_season_PSQL(data)
        return data

    def parse_betexplorer(self, data: pd.DataFrame) -> pd.DataFrame:
        data["MatchID"] = data["MatchID"].str[4:]
        data = self.parse_flashscore(data)
        data = self.parse_betexplorer_result(data)
        data = self.parse_betexplorer_date(data)
        return data

    def parse_isdb(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            data.loc[data['WDL'] == "W", 'WDL'] = int(1)
            data.loc[data['WDL'] == "L", 'WDL'] = int(2)
            data.loc[data['WDL'] == "D", 'WDL'] = int(0)
            data = data.astype({'WDL': 'int32'})
            data.rename(columns={'HT': 'Home', 'AT': 'Away', 'GD': 'SD', 'Sea': 'Season', 'Lge': 'League'}, inplace=True)
            return data
        except (KeyError, AttributeError):
            logger.framework_logger.error("Parsing was not successful")
            return data


    def remove_not_valid_results(self, data: pd.DataFrame):
        return data[(data["Result"] != '-') & (data["Result"] != '---')]

    def parse_score_PSQL(self, data: pd.DataFrame) -> pd.DataFrame:
        data["HS"] = pd.to_numeric(data["Result"].str.split("-", n=1).str[0]).astype(np.int64)
        data["AS"] = pd.to_numeric(data["Result"].str.split("-", n=1).str[1]).astype(np.int64)
        return data

    def parse_season_PSQL(self, data: pd.DataFrame) -> pd.DataFrame:
        data["Season"] = pd.to_numeric(data["Season"].str.split("/").str[0])
        return data

    def parse_betexplorer_result(self, data: pd.DataFrame) -> pd.DataFrame:
        conditions = [
            data["HS"] > data["AS"],  # Home win
            data["HS"] < data["AS"],  # Home loss
            data["HS"] == data["AS"]  # Draw
        ]

        choices = [1, 2, 0]

        data["WDL"] = np.select(conditions, choices, default=np.nan).astype('int32')
        data = data.dropna(subset=["WDL"])
        return data

    def parse_betexplorer_date(self, data: pd.DataFrame) -> pd.DataFrame:
        data["Date"] = data.apply(self.extract_date, axis=1)
        data = data.sort_values(by="Date").reset_index(drop=True)
        return data

    def extract_date(self, row):
        time_str = row["Time"]
        season = str(row["Season"])

        # Try to extract date with year if present
        import re
        match_with_year = re.search(r"(\d{1,2}\.\d{1,2}\.\s*\d{4})", time_str)
        if match_with_year:
            date_str = match_with_year.group(1).replace(" ", "")
            try:
                return pd.to_datetime(date_str, format="%d.%m.%Y", errors='raise')
            except:
                return pd.NaT
        else:
            # Extract just day.month and add season year
            match = re.search(r"(\d{1,2}\.\d{1,2}\.)", time_str)
            if match:
                date_str = match.group(1) + season
                try:
                    return pd.to_datetime(date_str, format="%d.%m.%Y", errors='raise')
                except:
                    return pd.NaT
            else:
                return pd.NaT
