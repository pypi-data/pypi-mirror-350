from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.simulation.Simulation import Simulation


class ThresholdUnderdogSimulation(Simulation):
    """
    A betting simulation that places bets on the underdog only if the odds exceed a threshold.

    Attributes:
    -----------
    stake : float
        The fixed amount to bet on each match.
    threshold : float
        The minimum odds required to place a bet.
    """

    def __init__(self, datawrapper: DataWrapper, stake: float = 1.0, threshold: float = 3.0):
        """
        Initialize the ThresholdUnderdogSimulation.

        Parameters:
        -----------
        datawrapper : DataWrapper
            A wrapper object that provides access to the match dataframe.
        stake : float
            The fixed bet amount per match (default is 1.0).
        threshold : float
            Minimum odds value required to place a bet (default is 3.0).
        """
        super().__init__(datawrapper)
        self.stake = stake
        self.threshold = threshold

    def run(self):
        """
        Run the underdog betting simulation with a minimum odds threshold.

        For each match, bet on the outcome with the highest odds if those odds exceed the threshold.
        """
        df = self.df.copy()
        odds_cols = {0: 'odds_1', 1: 'odds_X', 2: 'odd_2'}

        for _, row in df.iterrows():
            # Get all outcome odds
            odds_values = {k: row[v] for k, v in odds_cols.items()}
            underdog_outcome = max(odds_values, key=odds_values.get)
            odds = odds_values[underdog_outcome]

            # Only bet if odds exceed threshold
            if odds < self.threshold or odds <= 1:
                self.results.append(0)
                continue

            win = row['WDL'] == underdog_outcome
            ret = self.stake * (odds if win else 0) - self.stake
            self.results.append(ret)
