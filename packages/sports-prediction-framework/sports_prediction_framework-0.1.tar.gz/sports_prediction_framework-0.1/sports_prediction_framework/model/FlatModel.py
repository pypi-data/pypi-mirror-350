from sports_prediction_framework.model.NeuralModel import NeuralModel
from sports_prediction_framework.model.torch_model.TorchFlat import TorchFlat
from sports_prediction_framework.datawrapper.sport.MatchWrapper import MatchWrapper
import torch

from typing import Optional


class FlatModel(NeuralModel):

    def __init__(self,params: dict, pretrained_weights: Optional[torch.Tensor] = None, **kwargs) -> None:
        """
        Initialize the FlatModel. Creates an instance of the TorchFlat model and sets it up.

        Args:
            pretrained_weights (Optional[torch.Tensor]): Weights to initialize the model with,
                                                          if provided. Defaults to None.
            **kwargs: Additional keyword arguments passed to the parent class initializer.
        """
        # Initialize the TorchFlat model with optional pretrained weights
        super().__init__(**kwargs)
        self.params = params
        self.pretrained_weights = pretrained_weights

        self.model = TorchFlat(pretrained_weights)
        self.set_params(params)

        # Call the complex initialization of the model to set up the layers
        self.model.complex_init()

    def set_parameters_from_wrapper(self, wrapper: MatchWrapper) -> None:
        """
        Adjust the model parameters based on the provided MatchWrapper.

        Args:
            wrapper (MatchWrapper): The wrapper that contains match-related data used to
                                     configure the model (e.g., number of teams).
        """
        # Set model parameters using data from the wrapper (e.g., number of teams)
        self.model.set_parameters_from_wrapper(wrapper)

    def reset_state(self):
        self.model = TorchFlat(self.pretrained_weights)
        self.set_params(self.params)

        # Call the complex initialization of the model to set up the layers
        self.model.complex_init()
