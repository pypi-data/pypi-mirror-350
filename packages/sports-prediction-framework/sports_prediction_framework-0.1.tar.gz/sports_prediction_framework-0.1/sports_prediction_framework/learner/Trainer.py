from sports_prediction_framework.model.Model import *
from sports_prediction_framework.datawrapper.DataWrapper import *
class Trainer:

    def __init__(self, model: Model = None):
        """
        Initialize the Trainer with a model instance.

        Args:
            model (Model, optional): The model to be trained.
        """
        self.model = model

    def compute(self, dataset: DataWrapper):
        """
        Trigger the training process on the provided dataset.
        """
        self.train(dataset)

    def train(self, wrapper: DataWrapper):
        """
        Train the model using features and labels extracted from the wrapper.

        Args:
            wrapper (DataWrapper): The dataset wrapper containing features and labels.
        """
        if not self.model.in_cols:
            features = wrapper.get_features()
        else:
            features = wrapper.get_dataframe()[self.model.in_cols]

        # Let the model extract additional parameters from the data wrapper if needed
        self.model.set_parameters_from_wrapper(wrapper)

        # Fit the model on the selected features and labels
        self.model.fit(features, wrapper.get_labels())

    def reset_state(self):
        """
        Reset the internal state of the model (if any).
        """
        self.model.reset_state()
