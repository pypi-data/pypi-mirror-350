from sports_prediction_framework.model.Model import *
import sklearn
from sklearn.base import is_classifier, is_regressor
from sklearn.base import BaseEstimator
from typing import Type


class ScikitModel(Model):
    """
    A wrapper for scikit-learn estimators that integrates seamlessly into a broader modeling interface.

    This class handles preprocessing of labels and dynamically selects between `predict` and
    `predict_proba` based on the type of model and its capabilities.

    Parameters
    ----------
    model_class : Type[BaseEstimator]
        A scikit-learn model class (e.g., `RandomForestClassifier`, `LinearRegression`).
    **model_params : dict
        Parameters to pass to the model class constructor.

    Attributes
    ----------
    scikit_model : BaseEstimator
        An instance of the scikit-learn estimator.
    is_classifier : bool
        Flag indicating whether the estimator is a classifier.
    """

    def __init__(self, model_class: Type[BaseEstimator], **model_params):
        self.scikit_model = model_class(**model_params)
        self.is_classifier = is_classifier(self.scikit_model)

    def fit(self, features: pd.DataFrame, labels: pd.DataFrame):
        """
        Fit the scikit-learn model to the provided features and labels.

        Parameters
        ----------
        features : pd.DataFrame
            DataFrame of shape (n_samples, n_features) containing the input features.

        labels : pd.DataFrame
            DataFrame of shape (n_samples, 1) containing the target values.
            Will be converted to a Series internally.

        Raises
        ------
        AssertionError
            If the `labels` DataFrame does not contain exactly one column.
        """
        assert labels.shape[1] == 1
        if labels.shape[0] == 1:
            labels = pd.Series(labels.squeeze())
        else :
            labels = labels.squeeze()
        self.scikit_model.fit(features, labels)

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Make predictions on new data using the trained model.

        For classifiers with `predict_proba` support, returns class probabilities.
        Otherwise, falls back to `predict()`.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame of shape (n_samples, n_features) containing the input features.

        Returns
        -------
        np.ndarray
            Array of predictions or class probabilities.
        """
        if self.is_classifier and hasattr(self.scikit_model, "predict_proba"):
            return self.scikit_model.predict_proba(data)
        if hasattr(self.scikit_model, "predict"):
            return self.scikit_model.predict(data)

    def reset_state(self):
        """
        Reset the internal scikit-learn model to its initial untrained state.

        Uses `sklearn.base.clone` to create a fresh copy of the estimator with the same parameters.
        """
        self.scikit_model = sklearn.base.clone(self.scikit_model)

