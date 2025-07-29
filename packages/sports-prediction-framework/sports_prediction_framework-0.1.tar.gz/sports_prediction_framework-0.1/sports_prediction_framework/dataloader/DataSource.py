from sports_prediction_framework.dataloader.Connector import Connector
from sports_prediction_framework.datawrapper.SportType import SportType
import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import select


class DataSource:
    """
    Provides an interface for querying a PostgreSQL database with optional parsing based on sport type.
    Can connect either directly or via SSH tunneling and supports multiple query types.
    """

    def __init__(self, sport_type: SportType = None, via_ssh=True):
        """
        Initializes the DataSource and establishes a database connection.

        Args:
            sport_type (SportType, optional): If provided, sets up a parser specific to the sport.
            via_ssh (bool): If True, establishes the connection through SSH tunneling.
        """
        self.con = Connector()
        self.db_type = self.con.config['DB_NAME']

        if sport_type is not None:
            self.parser = sport_type.get_parser()()

        if via_ssh:
            self.con.connect_to_db_via_ssh()
        else:
            self.con.connect_to_db()

    def plain_query(self, query: str) -> pd.DataFrame:
        """
        Executes a raw SQL query directly.
        WARNING: This method does not sanitize inputs and is vulnerable to SQL injection. Use with caution.

        Args:
            query (str): Raw SQL query string.

        Returns:
            pd.DataFrame: Query results.
        """
        return pd.read_sql_query(query, con=self.con.get_engine())

    def parse_data(self, df: pd.DataFrame):
        """
        Parses the DataFrame according to the parser configured for the current database type.

        Args:
            df (pd.DataFrame): Raw query results.

        Returns:
            pd.DataFrame: Parsed DataFrame.
        """
        match self.db_type:
            case "bet":
                return self.parser.parse_isdb(df)
            case "flashscore":
                return self.parser.parse_flashscore(df)
            case "betexplorer":
                return self.parser.parse_betexplorer(df)
            case _:
                return df

    def query(self, schema_name, table_name, filter_func) -> pd.DataFrame:
        """
        Executes a filtered SQL query and parses the result based on the database type.

        Args:
            schema_name (str): Schema name.
            table_name (str): Table name.
            filter_func (Callable): Filter function to apply on table columns.

        Returns:
            pd.DataFrame: Parsed query result.
        """
        metadata = MetaData(schema=schema_name)
        table = Table(table_name, metadata, autoload_with=self.con.eng, schema=schema_name)
        query = select(table).filter(filter_func(table.c))
        df = pd.read_sql(query, self.con.session.bind)
        return self.parse_data(df)

    def query_no_parse(self, schema_name, table_name, filter_func) -> pd.DataFrame:
        """
        Executes a filtered SQL query without parsing the result.

        Args:
            schema_name (str): Schema name.
            table_name (str): Table name.
            filter_func (Callable): Filter function to apply on table columns.

        Returns:
            pd.DataFrame: Raw query result.
        """
        metadata = MetaData(schema=schema_name)
        table = Table(table_name, metadata, autoload_with=self.con.eng, schema=schema_name)
        query = select(table).filter(filter_func(table.c))
        df = pd.read_sql(query, self.con.session.bind)
        return df

    def preview_query(self, schema_name, table_name, filter_func) -> pd.DataFrame:
        """
        Retrieves a limited preview (5 rows) of the query results.

        Args:
            schema_name (str): Schema name.
            table_name (str): Table name.
            filter_func (Callable): Filter function to apply on table columns.

        Returns:
            pd.DataFrame: Preview of the query result.
        """
        metadata = MetaData(schema=schema_name)
        table = Table(table_name, metadata, autoload_with=self.con.eng, schema=schema_name)
        query = select(table).filter(filter_func(table.c)).limit(5)
        df = pd.read_sql(query, self.con.session.bind)
        return df

    def query_distinct(self, schema_name, table_name, filter_func, distinct_cols=None) -> pd.DataFrame:
        """
        Executes a query that returns distinct rows based on specified columns.

        WARNING: This uses PostgreSQL-specific `DISTINCT ON` functionality.

        Args:
            schema_name (str): Schema name.
            table_name (str): Table name.
            filter_func (Callable): Filter function to apply on table columns.
            distinct_cols (list, optional): Columns to apply DISTINCT ON.

        Returns:
            pd.DataFrame: Resulting DataFrame with distinct rows.
        """
        metadata = MetaData(schema=schema_name)
        table = Table(table_name, metadata, autoload_with=self.con.eng, schema=schema_name)

        if distinct_cols:
            query = select(table).distinct(*[table.c[col] for col in distinct_cols]).filter(filter_func(table.c))
        else:
            query = select(table).filter(filter_func(table.c))

        df = pd.read_sql(query, self.con.session.bind)
        return df

    def close(self):
        """
        Closes the database session and SSH tunnel (if used).
        """
        self.con.close()

