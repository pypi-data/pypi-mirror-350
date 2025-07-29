from sports_prediction_framework.transformer.Scope import Scope, EnumScope
from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from abc import ABC, abstractmethod


class ScopeSelector(ABC):
    def __init__(self, scope: Scope) -> None:
        self.scope = scope

    @abstractmethod
    def transform(self, dataset: DataWrapper) -> DataWrapper:
        pass

    @abstractmethod
    def __str__(self):
        pass

    def update(self):
        self.scope.shift()

    def holds(self):
        return self.scope.inside()

    def reset_state(self):
        self.scope.reset_state()

    def current_state(self):
        return self.scope.current_state()



class WindowSelector(ScopeSelector):

    def __init__(self, scope: Scope) -> None:
        super(WindowSelector, self).__init__(scope)

    def transform(self, dataset: DataWrapper) -> DataWrapper:
        data = dataset.get_dataframe()
        trans = data[(data[self.scope.col] >= self.scope.start) &
                     (data[self.scope.col] <= self.scope.start+self.scope.size)]
        return dataset.deepcopy(trans)

    def __str__(self):
        return str(self.scope.start) + ' ' + str(self.scope.start+self.scope.size)

    def current_state(self):
        return self.scope.current_state()

class EnumSelector(ScopeSelector):

    def __init__(self, scope: EnumScope):
        super().__init__(scope)
        self.scope = scope

    def transform(self, dataset: DataWrapper) -> DataWrapper:
        data = dataset.get_dataframe()
        trans = data.loc[data[self.scope.col] == self.scope.enum[self.scope.cur_index]]
        return dataset.deepcopy(trans)

    def __str__(self):
        return self.scope.enum[self.scope.cur_index]

    def current_state(self):
        return self.scope.current_state()