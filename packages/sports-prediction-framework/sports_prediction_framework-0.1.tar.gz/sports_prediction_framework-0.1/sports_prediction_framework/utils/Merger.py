from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
import pandas as pd
from typing import List


class Merger:
    """
    Merges multiple DataWrapper objects into a single, unified DataWrapper.

    This is useful for combining match data from multiple sources (e.g., different leagues)
    into a consolidated dataset, assuming all input wrappers are compatible in terms of
    schema and semantics.

    """

    def compute(self, wrappers: List[DataWrapper]) -> DataWrapper:
        """
        Merges a list of compatible DataWrapper instances into one.

        This method performs the following steps:
        - Collects all unique feature and label columns from the wrappers.
        - Merges the underlying DataFrames using common columns as join keys.
        - Creates a deep copy of the first wrapper and replaces its data with the merged DataFrame.
        - Combines team ID sets from all wrappers.

        Args:
            wrappers (List[DataWrapper]): A list of DataWrapper objects to be merged.
                                           All wrappers must have compatible schemas.

        Returns:
            DataWrapper: A new DataWrapper containing the merged data.
        """
        features = list(set.union(*(w.data_handler.feature_cols for w in wrappers)))
        labels = list(set.union(*(w.data_handler.label_cols for w in wrappers)))
        merged_df = self.merge([w.get_dataframe() for w in wrappers])
        merged_wrapper = wrappers[0].deepcopy(merged_df, features, labels)
        merged_wrapper.total_set_of_teams_ids = set.union(*(w.total_set_of_teams_ids for w in wrappers))
        return merged_wrapper

    def merge(self, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Merges multiple DataFrames using their common columns.

        All DataFrames must have overlapping columns and be compatible for joining.
        This method performs a series of inner merges on the shared columns across
        all DataFrames in the list.

        Args:
            dfs (List[pd.DataFrame]): A list of pandas DataFrames to be merged.

        Returns:
            pd.DataFrame: A single DataFrame resulting from merging all inputs.
        """
        if len(dfs) == 1:
            return dfs[0]
        pre = dfs[0]
        for d in dfs[1:]:
            common_cols = set(pre.columns).intersection(d.columns)
            pre = pre.merge(d, on=list(common_cols))
        return pre

