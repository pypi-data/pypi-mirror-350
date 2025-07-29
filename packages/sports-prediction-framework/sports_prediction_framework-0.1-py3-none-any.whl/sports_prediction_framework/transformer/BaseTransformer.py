import pandas as pd
from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper


class BaseTransformer:

    def __init__(self):
        self.id_map = {}

    def add_features(self, wrapper: DataWrapper, features) -> DataWrapper:
        dataset_c = wrapper.deepcopy()
        dataset_c.add_features(features)
        return dataset_c

    def names_to_ids(self, wrapper: DataWrapper):

        data = wrapper.data_handler
        names = set.union(*[set(data.dataframe[col]) for col in wrapper.name_columns])
        self.id_map.update({name: id for id, name in enumerate(sorted(names))})

        series = []
        data = wrapper.data_handler
        for namec, idc in zip(wrapper.name_columns, wrapper.name_id_columns):
            series.append(data.dataframe[namec].map(self.id_map.get).rename(idc))

        return self.add_features(wrapper, pd.concat(series, axis=1))

    def remove_small_seasons(self, wrapper: DataWrapper, min_teams: int):
        """
        Removes seasons from the DataFrame in DataWrapper where the number of unique teams is less than min_teams.

        Args:
            wrapper (DataWrapper): An instance of DataWrapper containing the DataFrame.
            min_teams (int): The minimum number of unique teams required to keep a season.

        Returns:
            DataWrapper: The modified DataWrapper with small seasons removed.
        """
        league_column = 'League'
        season_column = 'Season'
        to_be_removed = []
        for group_values,season in wrapper.get_dataframe().groupby([league_column,season_column]):
            if len(set(season['HID']).union(set(season['AID']))) < min_teams:
                to_be_removed.append(group_values)
        for rem in to_be_removed:
            wrapper.get_dataframe().drop(wrapper.get_dataframe()[(wrapper.get_dataframe()[league_column] == rem[0]) &
                                         (wrapper.get_dataframe()[season_column] == rem[1])].index,
                                         inplace=True)
        return wrapper


    def get_date_from_time(self, wrapper:DataWrapper) -> DataWrapper:
        """
        Extracts and converts dates from the 'Time' column in the DataFrame, accounting for season transitions.

        Args:
            wrapper (DataWrapper): An instance of DataWrapper containing the DataFrame.

        Returns:
            DataWrapper: The modified DataWrapper with the 'Date' column updated.
        """

        seasons = []
        for _,season in wrapper.get_dataframe().groupby(['League','Season']):
            season['day'] = season['Time'].str.split('.').str[0]
            season['month'] = pd.to_numeric(season['Time'].str.split('.').str[1])
            season = season.sort_values(['month', 'day'])
            season['diff'] = season['month'].diff()
            try:
                min_index = season[season['diff']>1]['diff'].idxmin()
            except:
                min_index = season['month'].idxmin()
            season['Date'] = pd.to_datetime(season.loc[:min_index]['Time'] + (season.loc[:min_index]['Season']+1).apply(str), format="%d.%m.%Y", errors='coerce')
            season.loc[min_index:,'Date'] = pd.to_datetime(season.loc[min_index:]['Time'] + (season.loc[min_index:]['Season']).apply(str), format="%d.%m.%Y", errors='coerce')
            season = season[season['Date'].notnull()]
            seasons.append(season)

        wrapper.set_dataframe(pd.DataFrame(index=wrapper.get_dataframe().index, data=pd.concat(seasons)['Date']))
        return wrapper

    def get_first_odds(self, wrapper: DataWrapper) -> DataWrapper:
        """
        Modifies the DataFrame inside the DataWrapper to keep only the first betting odds for each event.

        Args:
            wrapper (DataWrapper): An instance of DataWrapper.

        Returns:
            wrapper
        """
        wrapper.get_dataframe().drop_duplicates(subset=["MatchID"], keep='last', inplace=True)
        return wrapper

    def get_latest_odds(self, wrapper: DataWrapper) -> DataWrapper:
        """
        Modifies the DataFrame inside the DataWrapper to keep only the last betting odds for each event.

        Args:
            wrapper (DataWrapper): An instance of DataWrapper.

        Returns:
            wrapper
        """
        wrapper.get_dataframe().drop_duplicates(subset=["MatchID"], keep='first', inplace=True)
        return wrapper

    def get_first_and_latest_odds(self, wrapper: DataWrapper)-> DataWrapper:
        """
        Modifies the DataFrame inside the DataWrapper to keep only the first and the last betting odds together.

        Args:
            wrapper (DataWrapper): An instance of DataWrapper.

        Returns:
            wrapper
        """
        dataframe_first = wrapper.get_dataframe().drop_duplicates(subset=["MatchID"], keep='first')
        dataframe_last = wrapper.get_dataframe().drop_duplicates(subset=["MatchID"], keep='last')

        dataframe_final = dataframe_first.append(dataframe_last)

        wrapper.set_dataframe(dataframe_final)
        return wrapper


