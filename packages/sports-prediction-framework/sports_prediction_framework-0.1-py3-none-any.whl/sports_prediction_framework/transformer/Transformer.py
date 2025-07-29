from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.transformer.BaseTransformer import BaseTransformer

class Transformer:
    transformations = {'names_to_ids':True, 'names_to_ids_scope':False, 'remove_small_seasons':False,
              'result_column':False, 'score_diff':False, 'round_column':False, 'date_from_time':False,
              'only_latest_odds': False, 'only_first_odds': False, 'first_and_latest_odds': False}

    base_transformer = BaseTransformer()



    def load_from_dict(self,transform_dict: dict):
        """
        Updates the `transformations` dictionary with key-value pairs from `transform_dict`.

        Args:
            transform_dict (dict): A dictionary containing transformation keys and their corresponding values.
        """

        for key, value in transform_dict.items():
            if key in self.transformations.keys():
                self.transformations[key] = value
            else:
                print(f"Invalid transformation {key}")


    def load_from_list(self, transform_list: list):
        """
        Sets the corresponding entries in the transformations dictionary to True for each element in transform_list.

        Args:
            transform_list (list): A list of transformation keys to be updated in the transformations dictionary.
        """
        for elem in transform_list:
            if elem in self.transformations.keys():
                self.transformations[elem] = True


    def transform(self, wrapper: DataWrapper):
        """
        Applies transformations to the wrapper based on the active flags in the `transformations` dictionary.

        Args:
            wrapper (DataWrapper): The data wrapper to be transformed.

        Returns:
            DataWrapper: The transformed data wrapper after applying the selected transformations.
        """
        t = self.transformations
        if t['names_to_ids']:
            wrapper = self.base_transformer.names_to_ids(wrapper)
        if t['date_from_time']:
            wrapper = self.base_transformer.get_date_from_time(wrapper)
        if t['only_first_odds']:
            wrapper = self.base_transformer.get_first_odds(wrapper)
        if t['only_latest_odds']:
            wrapper = self.base_transformer.get_latest_odds(wrapper)
        if t['first_and_latest_odds']:
            wrapper = self.base_transformer.get_first_and_latest_odds(wrapper)

        return wrapper