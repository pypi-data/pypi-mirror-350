from sports_prediction_framework.model.Model import Model
import pandas as pd
import numpy as np


class NeuralModel(Model):

    in_cols = ['HID', 'AID', 'HS', 'AS', 'Date']

    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)

    def fit(self, features: pd.DataFrame, labels: pd.DataFrame):
        self.model.fit(features, labels)

    def predict(self, data: pd.DataFrame, mode="test") -> np.ndarray:
        return self.model.predict(data)