from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.simulation.Simulation import Simulation


class EVSimulation(Simulation):
    """
    A betting simulation strategy based on Expected Value (EV).

    Bets are placed only on matches where the EV is positive, calculated as:
        EV = (prob * (odds - 1)) - (1 - prob)

    Attributes:
    -----------
    stake : float
        The fixed amount to bet on each qualified match.
    """

    def __init__(self, datawrapper: DataWrapper, stake: float = 1.0):
        """
        Initialize the EVSimulation.

        Parameters:
        -----------
        datawrapper : DataWrapper
            A wrapper object that provides access to the match dataframe.
        stake : float
            The fixed bet amount per qualified match (default is 1.0).
        """
        super().__init__(datawrapper)
        self.stake = stake

    def run(self):
        """
        Run the expected value betting simulation.

        A fixed stake is placed only if the EV for the predicted outcome is positive.
        """
        df = self.df.copy()
        odds_map = {0: 'odds_1', 1: 'odds_X', 2: 'odd_2'}

        for _, row in df.iterrows():
            pred = row['prediction']
            prob = row[pred]
            odds_col = odds_map[pred]
            odds = row[odds_col]

            if odds <= 1:
                self.results.append(0)
                continue

            # Calculate expected value
            ev = (prob * (odds - 1)) - (1 - prob)

            if ev > 0:
                win = row['WDL'] == pred
                ret = self.stake * (odds if win else 0) - self.stake
                self.results.append(ret)
            else:
                self.results.append(0)