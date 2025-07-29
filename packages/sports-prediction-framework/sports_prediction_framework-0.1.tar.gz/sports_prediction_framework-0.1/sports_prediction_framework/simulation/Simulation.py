from abc import ABC, abstractmethod
import pandas as pd

from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper


class Simulation(ABC):
    """
    Abstract base class for betting strategy simulations.

    Provides a standardized interface and shared functionality for evaluating
    betting strategies using model predictions, actual match outcomes, and odds.

    Attributes:
    -----------
    datawrapper : DataWrapper
        Object providing access to the underlying match dataframe.
    df : pandas.DataFrame
        Copy of the dataframe containing match data, including probabilities and results.
    results : list of float
        List of profit/loss values for each match in the simulation.
    """

    def __init__(self, datawrapper:DataWrapper):
        """
        Initialize the Simulation base class.

        Parameters:
        -----------
        datawrapper : DataWrapper
            A wrapper object that provides access to the match dataframe.

        Notes:
        ------
        Drops rows with NaN in any of the probability columns (0, 1, 2).
        Also creates a 'prediction' column based on the highest predicted probability
        among columns 0, 1, and 2, corresponding to draw, home win, and away win.
        """
        self.datawrapper = datawrapper
        self.df = datawrapper.get_dataframe().copy()

        # Ensure columns 0,1,2 are numeric
        for col in [0, 1, 2]:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # Drop rows with NaN in any of the probability columns
        self. df = self.df.dropna(subset=[0, 1, 2])


        # Predict the most likely outcome (0: draw, 1: home win, 2: away win)
        self.df["prediction"] = self.df[[0, 1, 2]].idxmax(axis=1).astype(int)

        self.results = []

    @abstractmethod
    def run(self):
        """
        Run the betting simulation strategy.

        This method must be implemented by subclasses to define how profits/losses
        are calculated and recorded in `self.results`.
        """
        pass

    def evaluate(self):
        """
        Evaluate the simulation's performance.

        Returns:
        --------
        dict
            A dictionary containing:
                - total_return : float
                - mean_return : float
                - std_return : float
                - sharpe_ratio : float
        """
        returns = pd.Series(self.results)
        total_return = returns.sum()
        mean_return = returns.mean()
        std_return = returns.std()
        sharpe_ratio = mean_return / std_return if std_return != 0 else float("nan")
        return {
            "total_return": total_return,
            "mean_return": mean_return,
            "std_return": std_return,
            "sharpe_ratio": sharpe_ratio
        }

    def summary(self):
        """
        Print a summary of evaluation metrics to the console.
        """
        evals = self.evaluate()
        print(f"Total Return:  {evals['total_return']:.2f}")
        print(f"Mean Return:   {evals['mean_return']:.4f}")
        print(f"Std Dev:       {evals['std_return']:.4f}")
        print(f"Sharpe Ratio:  {evals['sharpe_ratio']:.4f}")
