import optuna
from sports_prediction_framework.utils.Evaluation import Metric
from sports_prediction_framework.learner.Learner import Learner
from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.utils.Evaluation import evaluate_metrics
from typing import Dict, Any, Tuple, Optional
from typing import Any, Dict
import pandas as pd


class Optimizer:
    """
    A class for optimizing hyperparameters using Optuna.

    Attributes:
        wrapper (DataWrapper): Data handling object for training and evaluation.
        learner (Learner): Model wrapper that can be trained and evaluated.
        metric (Metric): Metric enum used for evaluation (e.g., Accuracy, F1 Score).
        search_space (dict): Dictionary defining the hyperparameter search space.
        n_trials (int): Number of trials to run during optimization.
        direction (str): Optimization direction ('maximize' or 'minimize').
        sampler (optuna.samplers.BaseSampler, optional): Sampler for Optuna study.
    """

    def __init__(
        self,
        wrapper: DataWrapper,
        learner: Learner,
        metric: Metric,
        search_space: Dict[str, Tuple],
        n_trials: int = 50,
        direction: str = "maximize",
        sampler: Optional[optuna.samplers.BaseSampler] = None,
    ):
        self.wrapper = wrapper
        self.learner = learner
        self.metric = metric
        self.search_space = search_space
        self.n_trials = n_trials
        self.direction = direction
        self.sampler = sampler
        self.study = None

    def run(self):
        """
        Runs the optimization process using Optuna.
        """
        self.study = optuna.create_study(direction=self.direction, sampler=self.sampler)
        self.study.optimize(self._objective, n_trials=self.n_trials)

    def _suggest_params(self, trial):
        """
        Suggests hyperparameter values for the current trial.

        Args:
            trial (optuna.trial.Trial): The current Optuna trial.

        Returns:
            dict: A dictionary of suggested hyperparameter values.
        """
        params = {}
        for name, (ptype, *args) in self.search_space.items():
            kwargs = {}
            if args and isinstance(args[-1], dict):
                kwargs = args[-1]
                args = args[:-1]
            suggest_fn = getattr(trial, f"suggest_{ptype}")
            params[name] = suggest_fn(name, *args, **kwargs)
        return params

    def _objective(self, trial):
        """
        Objective function for the Optuna optimization.

        Args:
            trial (optuna.trial.Trial): The trial object.

        Returns:
            float: The evaluation score based on the selected metric.
        """
        try:
            params = self._suggest_params(trial)
            self.learner.reset_state()
            self.learner.set_model_hyper_params(params)
            preds = self.learner.compute(self.wrapper)
            #print(preds.get_dataframe())
            metrics, _ = evaluate_metrics(preds.get_dataframe(), 'macro')
            print(metrics)

            if self.metric.value not in metrics:
                raise ValueError(f"Metric '{self.metric.value}' not found in evaluation results.")

            score = metrics[self.metric.value]
            if isinstance(score, pd.Series):
                score = score.item()
            print(f"Trial {trial.number}: {params}, {self.metric.value} = {score:.4f}")
            return score

        except Exception as e:
            print(f"Trial {trial.number} pruned due to error: {e}")
            raise optuna.TrialPruned()

    def best_params(self) -> Dict[str, Any]:
        """
        Returns the best hyperparameters found by the optimization.

        Returns:
            dict: Best hyperparameters if available, else an empty dictionary.
        """
        return self.study.best_params if self.study else {}

    def best_value(self) -> float:
        """
        Returns the best metric value achieved during the optimization.

        Returns:
            float: Best value if available, else NaN.
        """
        return self.study.best_value if self.study else float("nan")