from sports_prediction_framework.dataloader.DataSource import DataSource
from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.datawrapper.DataHandler import DataHandler
from sports_prediction_framework.datawrapper.SportType import SportType
import pandas as pd
class DataLoader:
    """
    A utility class for loading and wrapping data from a database using the DataSource and DataHandler interfaces.
    Provides class methods for querying, previewing, and post-processing data.
    """

    @classmethod
    def load(cls, schema_name: str, table_name: str, filter_func) -> pd.DataFrame:
        """
        Loads a DataFrame from the specified schema and table using a filter function.

        Args:
            schema_name (str): Name of the schema in the database.
            table_name (str): Name of the table to query.
            filter_func (Callable): A function used to filter the query.

        Returns:
            pd.DataFrame: The resulting DataFrame from the query.
        """
        ds = DataSource()
        df = ds.query(schema_name, table_name, filter_func)
        ds.close()
        return df

    @classmethod
    def load_distinct(cls, schema_name: str, table_name: str, filter_func, distinct_cols=None) -> pd.DataFrame:
        """
        Loads a DataFrame from the specified schema and table, optionally using distinct columns.

        Args:
            schema_name (str): Name of the schema in the database.
            table_name (str): Name of the table to query.
            filter_func (Callable): A function used to filter the query.
            distinct_cols (list, optional): Columns to apply distinct selection on.

        Returns:
            pd.DataFrame: The resulting DataFrame from the query.
        """
        ds = DataSource()
        df = ds.query(schema_name, table_name, filter_func)
        ds.close()
        return df

    @classmethod
    def preview(cls, schema_name: str, table_name: str, filter_func, distinct_cols=None) -> pd.DataFrame:
        """
        Loads a preview of the data using the preview_query method.

        Args:
            schema_name (str): Name of the schema in the database.
            table_name (str): Name of the table to preview.
            filter_func (Callable): A function used to filter the query.
            distinct_cols (list, optional): Columns to apply distinct selection on.

        Returns:
            pd.DataFrame: A preview of the data.
        """
        ds = DataSource()
        df = ds.preview_query(schema_name, table_name, filter_func)
        ds.close()
        return df

    @classmethod
    def load_and_wrap(cls, schema_name, table_name, filter_func, sport: SportType = None):
        """
        Loads data from the database and wraps it using the appropriate wrapper for the specified sport.

        Args:
            schema_name (str): Name of the schema.
            table_name (str): Name of the table.
            filter_func (Callable): A function used to filter the query.
            sport (SportType, optional): The sport type which determines the data wrapper to use.

        Returns:
            DataWrapper: A wrapped handler containing the queried data.
        """
        ds = DataSource(sport)
        df = ds.query(schema_name, table_name, filter_func)
        handler = DataHandler(df)
        wrapper = sport.get_wrapper()(handler)
        ds.close()

        return wrapper

    @classmethod
    def load_and_wrap_odds(cls, schema_name, table_name, filter_func, sport: SportType = None, bookmaker=None):
        """
        Loads match data along with corresponding betting odds and wraps it for the given sport.

        Args:
            schema_name (str): Name of the schema.
            table_name (str): Name of the match data table.
            filter_func (Callable): A function used to filter the match data.
            sport (SportType, optional): The sport type which determines the data wrapper to use.
            bookmaker (str, optional): The bookmaker name used to filter the odds table.

        Returns:
            DataWrapper: A wrapped handler containing the match and betting odds data.
        """
        ds = DataSource(sport)
        df = ds.query(schema_name, table_name, filter_func)

        bookie_func = lambda c: c.Bookmaker == bookmaker
        bets = ds.query_no_parse(schema_name, "Odds_1x2", bookie_func)
        bets = bets.rename(columns={"1": "odds_1", "X": "odds_X", "2": "odds_2"})

        cols_to_join = ["MatchID", "odds_1", "odds_X", "odds_2"]
        odds_subset = bets[cols_to_join]
        df = df.merge(odds_subset, on="MatchID", how="inner")
        df[["odds_1", "odds_X", "odds_2"]] = df[["odds_1", "odds_X", "odds_2"]].apply(pd.to_numeric, errors='coerce')

        handler = DataHandler(df)
        wrapper = sport.get_wrapper()(handler)
        ds.close()

        return wrapper

