import torch
from torch.nn import Embedding, ModuleList, Linear, LogSoftmax, Dropout
from torch_geometric.nn import GraphConv
import torch.nn as nn

from sports_prediction_framework.datawrapper.sport.MatchWrapper import MatchWrapper
from sports_prediction_framework.model.torch_model.TorchModule import TorchModule
class TorchGNN(TorchModule):
    """
    A Graph Neural Network model that uses team embeddings and match-based graph structure
    to predict match outcomes using PyTorch Geometric.
    """

    def __init__(self, graph):
        """
        Initializes the model with a given dynamic graph object.
        """
        super(TorchGNN, self).__init__()
        self.graph = graph
        self.num_teams = None
        self.embedding = None

    def complex_init(self):
        """
        Initializes the convolutional and dense layers based on architecture settings.
        """
        if self.architecture_type == 'rectangle':
            self.conv_dims = [self.conv_dim] * (self.n_conv + 1)
            self.dense_dims = [self.dense_dim] * self.n_dense

        self.activation = nn.ReLU()  # or another, configurable

        self.conv_layers = ModuleList(
            [GraphConv(self.embed_dim, self.conv_dims[0])] +
            [GraphConv(self.conv_dims[i], self.conv_dims[i + 1]) for i in range(self.n_conv - 1)]
        )

        self.lin_layers = ModuleList(
            [Linear(self.conv_dims[self.n_conv - 1] * 2, self.dense_dims[0])] +
            [Linear(self.dense_dims[i], self.dense_dims[i + 1]) for i in range(self.n_dense - 2)] +
            [Linear(self.dense_dims[self.n_dense - 2], self.out_dim)]
        )

        self.out = LogSoftmax(dim=1)
        self.drop = Dropout(p=0.1)

    def set_parameters_from_wrapper(self, wrapper: MatchWrapper):
        """
        Initializes team embeddings based on the number of teams in the dataset.
        """
        if self.num_teams is None:
            self.num_teams = wrapper.total_number_of_teams
            self.embedding = Embedding(self.num_teams, self.embed_dim)

    def forward(self, features, home, away):
        """
        Performs a forward pass using the current match features and graph structure.
        """
        key = features.iloc[0][self.graph.column][1]  # gets scalar value

        graph = self.graph.graphs[key]
        edge_index, edge_weight = graph.edge_index, graph.edge_weight

        x = torch.arange(self.num_teams, device=home.device)
        x = self.embedding(x)

        x = self.conv_layers[0](x, edge_index, edge_weight) if len(edge_weight) > 0 else self.conv_layers[0](x, edge_index)
        x = self.activation(x)
        x = self.drop(x)

        for i in range(self.n_conv - 1):
            conv = self.conv_layers[i + 1]
            x = conv(x, edge_index, edge_weight) if len(edge_weight) > 0 else conv(x, edge_index)
            x = self.activation(x)
            x = self.drop(x)

        x = torch.cat([x[home], x[away]], dim=1)

        for layer in self.lin_layers:
            x = self.activation(layer(x))
            x = self.drop(x)

        return self.out(x).reshape(-1, self.out_dim)

    def model_specific_computation(self, features, labels, batch_index):
        """
        Updates the graph edges based on the current batch's match outcomes.
        """
        _, home, away = self.get_features_batch(features, batch_index)
        result = self.get_labels_batch(labels, batch_index)
        self.graph.graphs[features[self.graph.column].iloc[0][1]].compute(home, away, result)

    def get_features_batch(self, features, batch_index):
        """
        Extracts home and away team indices from features for the current batch.
        """
        batch = features.iloc[batch_index:batch_index + self.batch_size]
        home = torch.from_numpy(batch['HID'].values.astype('int64'))
        away = torch.from_numpy(batch['AID'].values.astype('int64'))
        return features, home, away

    def get_labels_batch(self, labels, batch_index):
        """
        Extracts match result labels for the current batch.
        """
        return torch.from_numpy(labels.iloc[batch_index:batch_index + self.batch_size].values.astype('int64'))