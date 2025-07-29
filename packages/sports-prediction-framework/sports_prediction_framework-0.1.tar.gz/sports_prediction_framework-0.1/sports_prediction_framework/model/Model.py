import pandas as pd
from sports_prediction_framework.utils.MLFlowTracker import MLFlowTracker
import inspect
import numpy as np
from sports_prediction_framework.datawrapper.DataWrapper import *


class Model:

    in_cols = []
    model = None

    def __init__(self, **kwargs):
        self._init_params = self._get_init_params()

    def fit(self, features: pd.DataFrame, labels: pd.DataFrame):
        raise NotImplementedError

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        raise NotImplementedError

    def set_parameters_from_wrapper(self, wrapper:DataWrapper):
        pass

    def reset_state(self):
        raise NotImplementedError

    def set_params(self, params: dict):
        for key,value in params.items():
            setattr(self.model, key, value)

    def _get_init_params(self) -> dict:
        """
        Retrieve the constructor parameters of the model instance.

        Uses introspection to get arguments passed to __init__, except 'self'.

        Returns
        -------
        dict
            Dictionary of parameter names and values.
        """
        frame = inspect.currentframe()
        init_args = inspect.getargvalues(frame.f_back)
        params = {k: v for k, v in init_args.locals.items() if k != 'self'}
        return params

    def log_params(self) -> None:
        """
        Log the model's constructor parameters to MLflow using MLFlowTracker.

        Raises
        ------
        RuntimeError
            If MLFlowTracker has no active run.
        """
        MLFlowTracker.log_params(self._init_params)