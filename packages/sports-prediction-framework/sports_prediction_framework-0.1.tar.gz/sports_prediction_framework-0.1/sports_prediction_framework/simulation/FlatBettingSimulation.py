from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.simulation.Simulation import Simulation
import pandas as pd


class FlatBettingSimulation(Simulation):
    """
    Implements a flat betting strategy simulation.

    In this simulation, a fixed stake is placed on each match based on the
    model's predicted outcome. If the prediction is correct, the return is
    calculated as (odds - 1) * stake. If incorrect, the entire stake is lost.

    Attributes:
    -----------
    stake : float
        The fixed amount to bet on each match.
    """

    def __init__(self, datawrapper: DataWrapper, stake=1.0):
        """
        Initialize the FlatBettingSimulation.

        Parameters:
        -----------
        datawrapper : DataWrapper
            A wrapper object that provides access to the match dataframe.
        stake : float, optional (default=1.0)
            The fixed amount to wager on each prediction.
        """
        super().__init__(datawrapper)
        self.stake = stake

    def run(self):
        """
        Execute the flat betting simulation.

        For each row in the dataframe, places a bet on the predicted outcome.
        If the prediction matches the actual result, calculates profit based
        on the odds. Otherwise, records a loss equal to the stake.
        """
        for _, row in self.df.iterrows():
            pred = row["prediction"]
            actual = row["WDL"]

            # Select corresponding odds
            if pred == 1:
                odds = row["odds_1"]
            elif pred == 0:
                odds = row["odds_X"]
            elif pred == 2:
                odds = row["odds_2"]
            else:
                self.results.append(0)
                continue

            # Skip if odds are invalid
            if pd.isna(odds) or odds <= 1.0:
                self.results.append(0)
                continue

            # Calculate return
            if pred == actual:
                profit = (odds - 1) * self.stake
            else:
                profit = -self.stake

            self.results.append(profit)
