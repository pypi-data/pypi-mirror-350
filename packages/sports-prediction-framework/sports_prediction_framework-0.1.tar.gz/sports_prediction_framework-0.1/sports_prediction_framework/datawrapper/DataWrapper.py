from sports_prediction_framework.datawrapper.DataHandler import DataHandler
import pandas as pd


class DataWrapper:
    """
    A higher-level interface for interacting with a DataHandler.
    Can be extended by specialized wrappers for domain-specific logic (e.g., MatchWrapper, RaceWrapper).
    """

    season_column = 'Season'

    # These can be overridden in subclasses
    name_columns = None
    name_id_columns = None
    prediction_columns = None
    score_columns = None
    result_column = None

    def __init__(self, data_handler: DataHandler, home_advantage=None):
        """
        Initializes the DataWrapper with a DataHandler.

        Args:
            data_handler (DataHandler): Core data manager for handling features, labels, predictions.
            home_advantage (optional): Optional metadata (used in some subclasses).
        """
        self.data_handler = data_handler

    def get_dataframe(self):
        """
        Returns the underlying DataFrame from the DataHandler.

        Returns:
            pd.DataFrame: The dataset.
        """
        return self.data_handler.dataframe

    def set_dataframe(self, dataframe):
        """
        Sets a new DataFrame to the underlying DataHandler.

        Args:
            dataframe (pd.DataFrame): New data to set.
        """
        self.data_handler.dataframe = dataframe

    def get_features(self):
        """
        Returns the feature columns from the DataHandler.

        Returns:
            pd.DataFrame: DataFrame of feature columns.
        """
        return self.data_handler.get_features()

    def add_features(self, features, on=None):
        """
        Adds new features to the dataset.

        Args:
            features (pd.DataFrame): Feature columns to add.
            on (str or list, optional): Columns to join on. Defaults to index-based join.
        """
        self.data_handler.add_features(features, on)

    def add_features_from_csv(self, filename, index=None, on=None):
        """
        Loads features from a CSV file and joins them into the dataset.

        Args:
            filename (str): Path to the CSV file.
            index (str or int, optional): Column to use as the index.
            on (str or list, optional): Columns to join on.
        """
        dataframe = pd.read_csv(filename, index_col=index)
        self.add_features(dataframe, on)

    def get_labels(self):
        """
        Returns the label columns from the DataHandler.

        Returns:
            pd.DataFrame: DataFrame of label columns.
        """
        return self.data_handler.get_labels()

    def add_labels(self, labels):
        """
        Adds new labels to the dataset.

        Args:
            labels (pd.DataFrame): Label columns to add.
        """
        self.data_handler.add_labels(labels)

    def get_predictions(self):
        """
        Returns the prediction columns from the DataHandler.

        Returns:
            pd.DataFrame: DataFrame of prediction columns.
        """
        return self.data_handler.get_predictions()

    def add_predictions(self, predictions):
        """
        Adds new predictions to the dataset.

        Args:
            predictions (pd.DataFrame): Prediction columns to add.
        """
        self.data_handler.add_predictions(predictions)

    def add_columns(self, data):
        """
        Adds arbitrary columns to the dataset (not tracked as features/labels/predictions).

        Args:
            data (pd.DataFrame): Columns to add.
        """
        self.data_handler.add_columns(data)

    def get_columns(self, column_names):
        """
        Retrieves specified columns from the dataset.

        Args:
            column_names (list): List of column names to retrieve.

        Returns:
            pd.DataFrame: DataFrame with specified columns.
        """
        return self.data_handler.get_columns(column_names)

    def set_after_compute_values(self):
        """
        Hook method for subclasses to override.
        Called after features, labels, or predictions are added to recalculate derived values.
        """
        pass

    def empty(self):
        """
        Checks whether the underlying dataset is empty.

        Returns:
            bool: True if empty, False otherwise.
        """
        return self.get_dataframe().empty

    def deepcopy(self, dataframe: pd.DataFrame = None, feat_cols=None, label_cols=None):
        """
        Creates a deep copy of the wrapper with optionally a new DataFrame and column sets.

        Args:
            dataframe (pd.DataFrame, optional): New DataFrame to use.
            feat_cols (iterable, optional): Feature columns for the new wrapper.
            label_cols (iterable, optional): Label columns for the new wrapper.

        Returns:
            DataWrapper: A new instance of the same class with copied data.
        """
        return self.copy(self.data_handler.copy(dataframe, feat_cols, label_cols))

    def copy(self, data_handler: DataHandler = None):
        """
        Creates a shallow copy of this wrapper, optionally using a different DataHandler.

        Args:
            data_handler (DataHandler, optional): Alternate DataHandler to use.

        Returns:
            DataWrapper: A new instance of the same class with shared or replaced DataHandler.
        """
        if data_handler is None:
            new = self.__class__(self.data_handler)
        else:
            new = self.__class__(data_handler)

        for attribute_key in self.__dict__.keys():
            if attribute_key != 'data_handler':
                new.__dict__[attribute_key] = self.__dict__[attribute_key]

        return new

