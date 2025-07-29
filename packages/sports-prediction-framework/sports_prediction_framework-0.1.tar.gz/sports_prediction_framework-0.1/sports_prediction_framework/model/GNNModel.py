from torch.nn import LeakyReLU

from sports_prediction_framework.datawrapper.sport.MatchWrapper import MatchWrapper
from sports_prediction_framework.model.FlatModel import NeuralModel
from sports_prediction_framework.model.torch_model.TorchGNN import TorchGNN
from sports_prediction_framework.transformer.ScopeSelector import WindowSelector, EnumSelector
from sports_prediction_framework.transformer.Scope import ScopeExpander, ScopeRoller, EnumScope


class GNNModel(NeuralModel):

    in_cols = ['HID', 'AID', 'HS', 'AS', 'Date', 'League']
    name = 'gnn'
    default_parameters = {'embed_dim':10, 'n_conv':3, 'conv_dim':32, 'n_dense':5, 'dense_dim':8,
                             'activation':LeakyReLU(), 'architecture_type':'rectangle', 'out_dim':3}

    def __init__(self, graph, parameters=default_parameters, **kwargs):
        super(GNNModel, self).__init__()
        self.in_cols.append(graph.column)
        self.graph = graph
        self.model = TorchGNN(graph)
        self.set_params(parameters)

        self.model.complex_init()

    def set_parameters_from_wrapper(self, wrapper:MatchWrapper):
        self.model.set_parameters_from_wrapper(wrapper)

    def get_train_scope(self, wrapper):
        min = wrapper.get_dataframe()[wrapper.season_column].min()
        window_selector = WindowSelector(ScopeExpander(wrapper,
                            {"start": min,"max": min + 1, "col": wrapper.season_column,"size": 1}))
        enum_selector = EnumSelector(EnumScope(wrapper, {"enum": wrapper.get_leagues(),"col": wrapper.league_column}))

        relevant_scope = [enum_selector,window_selector]
        return relevant_scope

    def get_test_scope(self, wrapper):
        min = wrapper.get_dataframe()[wrapper.season_column].min()
        window_selector = WindowSelector(ScopeRoller(wrapper,
                            {"start": min,"max": min + 1, "col": wrapper.season_column,"size": 1}))
        enum_selector = EnumSelector(EnumScope(wrapper, {"enum": wrapper.get_leagues(), "col": wrapper.league_column}))

        prediction_scope = [enum_selector, window_selector]
        return prediction_scope