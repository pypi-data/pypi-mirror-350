from sports_prediction_framework.model.Model import *
from sports_prediction_framework.model.Scikit import *


class Tester:
    """
    Handles prediction for a given model on a dataset wrapped by DataWrapper.
    """

    def __init__(self, model: Model = None):
        """
        Initializes the Tester with a model.

        Args:
            model (Model): The predictive model to be tested.
        """
        self.model = model

    def compute(self, dataset: DataWrapper) -> pd.DataFrame:
        """
        Alias for the test method, runs prediction on the dataset.

        Args:
            dataset (DataWrapper): Dataset wrapper containing features.

        Returns:
            pd.DataFrame: Predictions with index aligned to dataset.
        """
        return self.test(dataset)

    def test(self, wrapper: DataWrapper) -> pd.DataFrame:
        """
        Generates predictions from the model using the provided DataWrapper.

        Args:
            wrapper (DataWrapper): Dataset wrapper.

        Returns:
            pd.DataFrame: Predictions indexed by the original dataset index.
                          Columns depend on the model's output shape and type.
        """
        # Select features based on model's expected input columns
        if not self.model.in_cols:
            features = wrapper.get_features()
        else:
            features = wrapper.get_dataframe()[self.model.in_cols]

        # Scikit-learn model specific handling
        if isinstance(self.model, ScikitModel):
            if features.isnull().values.any():
                print('Features contain nulls or NaNs in scikit predicting')
                return pd.DataFrame()  # Return empty if invalid data

            preds = self.model.predict(features)

            # If multiclass/multilabel prediction, use class names as columns
            if preds.shape[1] > 1:
                cols = self.model.scikit_model.classes_
            else:
                # Use label columns from the wrapper if single-output
                cols = wrapper.data_handler.label_cols

            return pd.DataFrame(index=wrapper.get_dataframe().index, data=preds, columns=cols)
        else:
            # For other model types, just convert predictions to DataFrame
            preds = self.model.predict(features)
            return pd.DataFrame(index=wrapper.get_dataframe().index, data=preds)

