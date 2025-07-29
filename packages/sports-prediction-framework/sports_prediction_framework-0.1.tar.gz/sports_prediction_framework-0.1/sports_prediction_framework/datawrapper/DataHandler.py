import pandas as pd


class DataHandler:
    """
    A utility class for managing features, labels, and predictions within a pandas DataFrame.
    Provides methods for accessing, modifying, and copying the underlying data.
    """

    def __init__(self, dataframe: pd.DataFrame = None, feature_cols=None, label_cols=None, prediction_cols=None):
        """
        Initializes the DataHandler with a DataFrame and optional columns for features, labels, and predictions.

        Args:
            dataframe (pd.DataFrame, optional): The primary data container.
            feature_cols (iterable, optional): Column names to mark as features.
            label_cols (iterable, optional): Column names to mark as labels.
            prediction_cols (list, optional): Columns used to store predictions.
        """
        self.dataframe = dataframe
        self.prediction_cols = prediction_cols  # Columns created by learners for storing predictions

        self.label_cols = set(label_cols) if label_cols is not None else set()
        self.feature_cols = set(feature_cols) if feature_cols is not None else set()

    def get_dataframe(self):
        """
        Returns the underlying DataFrame.

        Returns:
            pd.DataFrame: The managed DataFrame.
        """
        return self.dataframe

    def set_dataframe(self, dataframe: pd.DataFrame):
        """
        Sets a new DataFrame as the underlying data container.

        Args:
            dataframe (pd.DataFrame): The new DataFrame to manage.
        """
        self.dataframe = dataframe

    def get_features(self):
        """
        Retrieves the feature columns from the DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing only feature columns.
        """
        return self.dataframe[self.feature_cols]

    def add_features(self, features, on=None):
        """
        Joins new feature columns into the DataFrame and updates the feature column set.

        Args:
            features (pd.DataFrame): New feature columns to add.
            on (str or list, optional): Column(s) to join on. Defaults to index-based join.
        """
        self.dataframe = self.dataframe.join(features, on=on) if on else self.dataframe.join(features)
        self.feature_cols.update(features.columns.tolist())

    def get_labels(self):
        """
        Retrieves the label columns from the DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing only label columns.
        """
        return self.dataframe[list(self.label_cols)]

    def add_labels(self, labels):
        """
        Joins new label columns into the DataFrame and updates the label column set.

        Args:
            labels (pd.DataFrame): New label columns to add.
        """
        self.dataframe = self.dataframe.join(labels)
        self.label_cols.update(labels.columns.tolist())

    def get_predictions(self):
        """
        Retrieves the prediction columns from the DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing prediction columns.
        """
        return self.dataframe[self.prediction_cols]

    def add_predictions(self, predictions):
        """
        Joins new prediction columns into the DataFrame and updates the prediction column list.

        Args:
            predictions (pd.DataFrame): New prediction columns to add.
        """
        self.dataframe = self.dataframe.join(predictions)
        if self.prediction_cols is None:
            self.prediction_cols = []
        self.prediction_cols += predictions.columns.tolist()

    def get_columns(self, columns):
        """
        Retrieves specified columns from the DataFrame.

        Args:
            columns (list): List of column names to retrieve.

        Returns:
            pd.DataFrame: DataFrame containing the specified columns.
        """
        return self.dataframe[columns]

    def add_columns(self, data):
        """
        Joins additional columns into the DataFrame. Does not update feature/label/prediction sets.

        Args:
            data (pd.DataFrame): Columns to add.
        """
        self.dataframe = self.dataframe.join(data)

    def copy(self, dataframe: pd.DataFrame = None, feat_cols=None, label_cols=None):
        """
        Creates a copy of the DataHandler, optionally with a new DataFrame and column sets.

        Args:
            dataframe (pd.DataFrame, optional): New DataFrame to copy. Defaults to current.
            feat_cols (iterable, optional): Feature columns for the new handler. Defaults to current.
            label_cols (iterable, optional): Label columns for the new handler. Defaults to current.

        Returns:
            DataHandler: A new DataHandler instance with the copied data and metadata.
        """
        if dataframe is None:
            dataframe = self.dataframe
        if feat_cols is None:
            feat_cols = self.feature_cols
        if label_cols is None:
            label_cols = self.label_cols

        return DataHandler(dataframe, feature_cols=feat_cols, label_cols=label_cols)


class DataMerger:
    @staticmethod
    def merge_data_handlers(self, handlers: [DataHandler]) -> DataHandler:
        merged = handlers[0].copy()
        merged.dataframe = pd.concat([handler.dataframe for handler in handlers], ignore_index=True)
        merged.dataframe.sort_index(inplace=True)
        return merged
