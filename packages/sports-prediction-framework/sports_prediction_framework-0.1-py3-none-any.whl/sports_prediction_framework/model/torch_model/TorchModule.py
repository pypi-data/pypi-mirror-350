import torch
import numpy as np
import pandas as pd
from typing import Tuple
from abc import ABC, abstractmethod


class TorchModule(torch.nn.Module, ABC):
    """
    Base class for PyTorch models that handles training and prediction logic.
    Intended to be subclassed with specific implementations of:
    - forward()
    - get_features_batch()
    - get_labels_batch()
    - model_specific_computation()
    """

    def __init__(self, **kwargs) -> None:
        """
         Initializes default training parameters.
         Subclasses can override these or pass them via kwargs.
         """
        super(TorchModule, self).__init__()
        self.print_info = False             # Whether to print info during training
        self.batch_size = 9                 # Mini-batch size
        self.epochs = 100                   # Number of training epochs
        self.train_loss = []                # Store average training loss per epoch
        self.train_accuracy = []            # Store average training accuracy per epoch
        self.lr = 0.0001                    # Learning rate

    @abstractmethod
    def forward(self, *args, **kwargs) -> torch.Tensor:
        """
        Must be implemented by subclass to define model forward pass.
        """
        pass

    @abstractmethod
    def get_features_batch(self, features: pd.DataFrame, start_index: int) -> Tuple:
        """
        Extract a batch of features from the full dataset.

        :param features: Full features DataFrame
        :param start_index: Start index of batch
        :return: Batch tuple (to be passed to forward)
        """
        pass

    @abstractmethod
    def get_labels_batch(self, labels: pd.DataFrame, start_index: int) -> torch.Tensor:
        """
        Extract corresponding labels for a feature batch.

        :param labels: Full labels DataFrame
        :param start_index: Start index of batch
        :return: Tensor of labels
        """
        pass

    @abstractmethod
    def model_specific_computation(self, features: pd.DataFrame, labels: pd.DataFrame, start_index: int) -> None:
        """
        Optional hook for any custom per-batch logic during training.

        :param features: Features DataFrame
        :param labels: Labels DataFrame
        :param start_index: Start index of the current batch
        """
        pass

    def fit(self, features: pd.DataFrame, labels: pd.DataFrame = None):
        """
        Trains the model on the given features and labels.

        :param features: DataFrame containing input features
        :param labels: DataFrame containing ground truth labels
        """
        criterion = torch.nn.NLLLoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)
        running_loss = []
        running_accuracy = []

        for epoch in range(self.epochs):
            acc = 0
            loss_value = 0.0
            optimizer.zero_grad()

            # Iterate over mini-batches
            for j in range(0, features.shape[0], self.batch_size):
                # Get input features and labels for the batch
                outputs = self(*self.get_features_batch(features, j))
                result = self.get_labels_batch(labels, j)

                # Compute loss and update weights
                loss = criterion(outputs, result)
                loss.backward()
                optimizer.step()
                loss_value += loss.item()

                # Compute number of correct predictions in batch
                _, predicted = torch.max(outputs.data, 1)
                correct = int((predicted == result).sum().item())
                running_accuracy.append(correct)
                acc += correct

                # Optional subclass hook for additional computation/logging
                self.model_specific_computation(features, labels, j)

            # Print training info per epoch
            if self.print_info:
                print(f"Epoch:{epoch}, train_loss:{loss_value:.5f}, train_acc:{acc / features.shape[0]:.5f}")

            running_loss.append(loss_value)

        # Compute overall training metrics across all epochs
        self.train_loss.append(sum(running_loss) / ((features.shape[0] / self.batch_size) * self.epochs))
        self.train_accuracy.append(sum(running_accuracy) / (features.shape[0] * self.epochs))

    def predict(self, data: pd.DataFrame, mode="test") -> np.ndarray:
        """
        Predicts output probabilities for the input data using the trained model.

        :param data: DataFrame containing input features
        :param mode: Optional flag for test/validation usage
        :return: Numpy array of predicted probabilities
        """
        predicted, outputs = self.get_predictions(data)
        return torch.exp(outputs).numpy()  # Convert log-probabilities to probabilities

    def get_predictions(self, matches) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Computes predicted classes and raw model outputs.

        :param matches: DataFrame containing input features
        :return: Tuple of predicted class indices and raw log-probabilities
        """
        outputs = self.get_probabilities(matches)
        _, predicted = torch.max(torch.exp(outputs.data), 1)  # Get class with highest probability
        return predicted, outputs

    def get_probabilities(self, matches):
        """
        Computes raw model outputs (log-probabilities) using forward pass.

        :param matches: DataFrame with match data, must include columns 'HID' and 'AID'
        :return: Tensor of log-probabilities for each match
        """
        self.eval()  # Set model to eval mode (disables dropout, etc.)

        home = torch.from_numpy(matches['HID'].values.astype('int64'))
        away = torch.from_numpy(matches['AID'].values.astype('int64'))

        with torch.no_grad():  # Disable gradient tracking
            outputs = self(matches, home, away)

        self.train()  # Switch back to training mode
        return outputs


