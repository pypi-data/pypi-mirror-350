from sports_prediction_framework.simulation.Simulation import Simulation
import numpy as np


class KellySimulation(Simulation):
    """
    Kelly betting simulation.

    Bets a fraction of the bankroll based on the Kelly criterion, maximizing the
    expected logarithmic growth of wealth.

    Attributes
    ----------
    data_wrapper : DataWrapper
        DataWrapper instance containing the data to simulate on.
    initial_bankroll : float
        The starting bankroll, default is 1.0.

    """

    def __init__(self, data_wrapper, initial_bankroll=1.0):
        """
        Initialize KellySimulation.

        Parameters
        ----------
        data_wrapper : DataWrapper
            DataWrapper instance holding the data.
        initial_bankroll : float, optional
            Starting bankroll (default is 1.0).
        """
        super().__init__(data_wrapper)
        self.initial_bankroll = initial_bankroll

    def run(self):
        df = self.df.copy()
        bankroll = self.initial_bankroll
        self.bankroll_history = [bankroll]

        odds_map = {0: 'odds_1', 1: 'odds_X', 2: 'odd_2'}

        for _, row in df.iterrows():
            pred = row['prediction']
            prob = row[pred]
            odds = row[odds_map[pred]]

            edge = prob * (odds - 1) - (1 - prob)
            fraction = max(edge / (odds - 1), 0) if odds > 1 else 0

            bet_amount = bankroll * fraction

            win = 1 if row['WDL'] == pred else 0
            ret = bet_amount * (odds if win else 0) - bet_amount

            bankroll += ret
            self.bankroll_history.append(bankroll)
            self.results.append(ret)