import pandas as pd
from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.learner.Trainer import Trainer
from sports_prediction_framework.learner.Tester import Tester
from sports_prediction_framework.transformer.DataSelector import DataSelector
from sports_prediction_framework.utils.Merger import Merger


class Learner:
    """
    Coordinates the training and testing of a model using a Trainer and Tester on data segmented by a DataSelector (scope).
    """

    def __init__(self, trainer: Trainer = None, tester: Tester = None, scope: DataSelector = None, **kwargs):
        """
        Initializes the Learner.

        Args:
            trainer (Trainer): Component responsible for training the model.
            tester (Tester): Component responsible for generating predictions.
            scope (DataSelector): Object that defines training and testing subsets.
        """
        self.trainer = trainer
        self.tester = tester
        self.scope = scope
        if self.scope is None:
            raise ValueError("Scope has to be set!")

    def compute(self, wrapper: DataWrapper) -> DataWrapper:
        """
        Executes the train-test workflow and attaches predictions to the wrapper.

        Args:
            wrapper (DataWrapper): Dataset to train/test on.

        Returns:
            DataWrapper: Copy of the input wrapper with added predictions.
        """
        features = self.train_test(wrapper)
        if features is None:
            return wrapper
        features = features[~features.index.duplicated(keep='first')]
        pwrapper = wrapper.deepcopy()
        pwrapper.add_predictions(features)
        return pwrapper

    def train_test(self, dataset: DataWrapper) -> pd.DataFrame:
        """
        Performs the train-test split, fits the model, and returns predictions.

        Args:
            dataset (DataWrapper): Complete dataset.

        Returns:
            pd.DataFrame: Predictions from the test set.
        """
        train_wrapper = self.scope.transform_train(dataset)
        test_wrapper = self.scope.transform_test(dataset)
        if train_wrapper.empty() or test_wrapper.empty():
            return pd.DataFrame()
        self.train(train_wrapper)
        return self.test(test_wrapper)

    def train(self, dataset: DataWrapper):
        """
        Trains the model using the provided dataset.

        Args:
            dataset (DataWrapper): Training data.

        Raises:
            ValueError: If the dataset is empty.
        """
        if self.trainer is not None:
            if not dataset.get_dataframe().empty:
                self.trainer.train(dataset)
            else:
                raise ValueError("Missing data!")

    def test(self, dataset: DataWrapper) -> pd.DataFrame:
        """
        Tests the model using the provided dataset and returns predictions.

        Args:
            dataset (DataWrapper): Testing data.

        Returns:
            pd.DataFrame: Model predictions.

        Raises:
            ValueError: If the dataset is empty.
        """
        if self.tester is not None:
            if not dataset.get_dataframe().empty:
                return self.tester.test(dataset)
            else:
                raise ValueError("Missing data!")
        return None

    def set_model_hyper_params(self, params):
        """
        Sets hyperparameters on the underlying model in both the trainer and tester.

        Args:
            params (dict): Dictionary of model hyperparameters.
        """
        self.trainer.model.set_params(params)
        self.tester.model.set_params(params)

    def reset_state(self):
        """
        Resets the internal state of the trainer.
        """
        self.trainer.reset_state()

    def update(self):
        """
        Updates the state of the DataSelector (e.g., for time-based iteration).
        """
        self.scope.update()


class LearnerWithoutScope(Learner):
    """
    Simplified Learner that uses the entire dataset for both training and testing.
    """

    def __init__(self, trainer: Trainer = None, tester: Tester = None, **kwargs):
        """
        Initializes the LearnerWithoutScope. No scope is required.

        Args:
            trainer (Trainer): Trainer component.
            tester (Tester): Tester component.
        """
        super().__init__(trainer, tester, None, **kwargs)

    def train_test(self, dataset: DataWrapper) -> pd.DataFrame:
        """
        Trains and tests the model on the same dataset.

        Args:
            dataset (DataWrapper): Full dataset.

        Returns:
            pd.DataFrame: Predictions.
        """
        self.train(dataset)
        return self.test(dataset)


class UpdatingLearner(Learner):
    """
    A Learner that iteratively trains and tests the model while a condition in the DataSelector holds.
    Can coordinate multiple internal learners and merge their predictions.
    """

    def __init__(
        self,
        trainer: Trainer = None,
        tester: Tester = None,
        scope: DataSelector = None,
        learners: list = None
    ):
        """
        Initializes the UpdatingLearner.

        Args:
            trainer (Trainer): Trainer component.
            tester (Tester): Tester component.
            scope (DataSelector): DataSelector for iterative training/testing.
            learners (list): Optional list of nested Learner instances to coordinate.
        """
        self.learners = learners if isinstance(learners, list) else ([learners] if learners else [])
        self.merger = Merger() if self.learners else None
        super().__init__(trainer, tester, scope)

    def train_test(self, wrapper: DataWrapper):
        """
        Iteratively trains and tests as long as the scope condition holds.
        If inner learners are provided, they are run in parallel and their predictions merged.

        Args:
            wrapper (DataWrapper): Full dataset.

        Returns:
            pd.DataFrame: Concatenated predictions from all iterations.
        """
        outputs = []
        copy = wrapper.deepcopy()

        while self.scope.holds():
            if self.learners:
                wrappers = []
                for learner in self.learners:
                    wrappers.append(learner.compute(copy))
                    learner.update()
                wrapper = self.merger.compute(wrappers)

            outputs.append(super().train_test(wrapper))
            self.update()

        if self.tester is not None and outputs:
            return pd.concat(outputs)
        return pd.DataFrame() if outputs else None

    def reset_state(self):
        """
        Resets state of all inner learners, the scope, and the trainer.
        """
        if self.learners:
            for learner in self.learners:
                learner.reset_state()
        self.scope.reset_state()
        self.trainer.reset_state()

