import torch
import numpy as np
from sports_prediction_framework.transformer.ScopeSelector import ScopeSelector
from sports_prediction_framework.datawrapper.sport.MatchWrapper import MatchWrapper
from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from torch_geometric.data import Data

class TeamStrengthGraph:
    """
    A class that represents a time-aware team interaction graph for use in GNN models,
    specifically for encoding team matchups and their outcomes over time.

    Attributes:
        scope: A scope object used for iterative transformation of the input data.
        column (str): The data column used to distinguish graphs (e.g., by league).
        graphs (dict): A dictionary of computed graphs keyed by scope state.
    """

    def __init__(self, scope: ScopeSelector):
        """
        Initialize the TeamStrengthGraph.

        Args:
            scope: A scope object that provides access to transformed data and state.
        """
        self.scope = scope
        self.column = 'League'
        self.graphs = {}

    def compute(self, wrapper: DataWrapper):
        """
        Computes graphs for each state in the scope and stores them internally.

        Args:
            wrapper: A data wrapper object used for transformation.
        """
        while self.scope.holds():
            trans = self.scope.transform(wrapper)
            if isinstance(trans, MatchWrapper):
                num_teams = len(trans.get_set_of_teams())
                num_matches = len(trans.get_dataframe().index)
                key = self.scope.current_state()[1][0]
                print(num_teams)
                self.graphs[key] = self.Graph(num_teams, num_matches)
                #print(key)
                self.scope.update()



    class Graph:
        """
        A class representing a directed temporal graph of team interactions.

        Attributes:
            num_matches (int): Total number of matches in the dataset.
            edge_index (torch.Tensor): Tensor of shape [2, num_edges] containing directed edges.
            edge_weight (torch.Tensor): Tensor of edge weights based on recency.
            edge_time (torch.Tensor): Matrix of last match times between teams.
            curr_time (int): Current time step (match index).
            num_teams (int): Total number of unique teams.
        """

        def __init__(self, num_teams: int, num_matches: int):
            """
            Initializes a new Graph.

            Args:
                num_teams (int): Number of unique teams.
                num_matches (int): Total number of matches (for normalization).
            """
            self.num_matches = num_matches
            self.edge_index = torch.empty((2, 0), dtype=torch.long)
            self.edge_weight = torch.empty((0,), dtype=torch.float)
            self.edge_time = torch.full((num_teams, num_teams), float('nan'))
            self.curr_time = 0
            self.num_teams = num_teams

        def compute(self, home: np.ndarray, away: np.ndarray, result: np.ndarray, time_weighing: str = "linear") -> Data:
            """
            Updates the graph with new match results and returns a PyTorch Geometric Data object.

            Args:
                home (np.ndarray): Array of encoded home team indices.
                away (np.ndarray): Array of encoded away team indices.
                result (np.ndarray): Array of match results (0=draw, 1=home win, 2=away win).
                time_weighing (str): Time decay strategy, either "linear" or "exponential".

            Returns:
                Data: PyTorch Geometric graph object with edge_index and edge_weight.
            """
            self.update_edge_time(home, away, result)
            self.update_edge_index()
            self.calculate_edge_weight(time_weighing)
            self.curr_time += 1
            return self.build_graph()

        def update_edge_time(self, home: np.ndarray, away: np.ndarray, result: np.ndarray):
            """
            Updates the edge_time matrix to record when matches occurred between teams.

            Args:
                home (np.ndarray): Encoded indices of home teams.
                away (np.ndarray): Encoded indices of away teams.
                result (np.ndarray): Match results (0=draw, 1=home win, 2=away win).
            """

            winning_team = np.array([], dtype=np.int64)
            losing_team = np.array([], dtype=np.int64)

            idx = np.where(result == 1)[0]
            winning_team = np.append(winning_team, home[idx])
            losing_team = np.append(losing_team, away[idx])

            idx = np.where(result == 2)[0]
            winning_team = np.append(winning_team, away[idx])
            losing_team = np.append(losing_team, home[idx])

            idx = np.where(result == 0)[0]
            winning_team = np.append(winning_team, home[idx])
            losing_team = np.append(losing_team, away[idx])
            winning_team = np.append(winning_team, away[idx])
            losing_team = np.append(losing_team, home[idx])

            self.edge_time[losing_team, winning_team] = self.curr_time

        def update_edge_index(self):
            """
            Updates the edge_index tensor with current directed edges.
            """
            src, dst = np.where(~np.isnan(self.edge_time))
            self.edge_index = torch.tensor([src, dst], dtype=torch.long)

        def calculate_edge_weight(self, time_weighing: str = "linear"):
            """
            Computes edge weights based on time decay since the last match.

            Args:
                time_weighing (str): "linear" or "exponential" decay of influence.
            """
            if self.edge_index.numel() > 0:
                from_nodes = self.edge_index[0].numpy()
                to_nodes = self.edge_index[1].numpy()

                # Work in NumPy
                prev_edge_time = np.array(self.edge_time[from_nodes, to_nodes], copy=True)
                prev_edge_time[np.isnan(prev_edge_time)] = self.curr_time

                if time_weighing == "linear":
                    weights = 1 - ((self.curr_time - prev_edge_time) / self.num_matches)
                elif time_weighing == "exponential":
                    weights = np.exp(- (self.curr_time - prev_edge_time))
                else:
                    raise ValueError(f"Unknown time weighing strategy: {time_weighing}")

                self.edge_weight = torch.tensor(weights, dtype=torch.float32)
            else:
                self.edge_weight = torch.tensor([], dtype=torch.float32)

        def build_graph(self) -> Data:
            """
            Builds and returns a PyTorch Geometric Data object from the current state.

            Returns:
                Data: A graph with edge_index, edge_attr (weights), and num_nodes.
            """
            return Data(
                edge_index=self.edge_index,
                edge_attr=self.edge_weight,
                num_nodes=self.num_teams
            )
