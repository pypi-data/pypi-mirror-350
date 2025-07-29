from abc import ABC, abstractmethod
from datetime import timedelta
from sports_prediction_framework.datawrapper.DataWrapper import DataWrapper
from sports_prediction_framework.utils.AttributeSetter import AttributeSetter
import pandas as pd


class Scope(ABC):

    def __init__(self, wrapper: DataWrapper = None, parameters=None):
        self.wrapper = wrapper
        self.parameters = parameters
        AttributeSetter.set_attributes(self, parameters)

    def shift(self):
        pass

    def inside(self):
        pass

    def reset_state(self):
        pass

    def current_state(self):
        pass






class WindowScope(Scope):

    #Stride is where should it jump to.

    default_parameters = {'col': 'Season', 'start': 2000, 'max': 2005, 'size': 1, 'stride': 2}

    def __init__(self, wrapper: DataWrapper = None, parameters=default_parameters):
        super().__init__(wrapper, parameters)
        if self.parameters is not None:
            if 'start' in self.parameters:
                # just for easier understanding of this branching
                self.start = self.parameters['start']
            elif self.wrapper is not None and self.parameters['col'] is not None:
                # set start from wrapper
                self.start = self.wrapper.get_dataframe()[self.parameters['col']].min()
            if 'max' in self.parameters:
                self.max = self.parameters['max']
            elif self.wrapper is not None:
                self.max = self.wrapper.get_dataframe()[self.parameters['col']].max()
            self.orig_start = self.start
            self.orig_size = self.size

    def reset_state(self):
        self.start = self.orig_start
        self.size = self.orig_size

    def current_state(self):
        if type(self.start) is int or type(self.size) is int:
            return self.col, (self.start, self.start + self.size + timedelta(days=1).days)
        return self.col, (self.start, self.start + self.size + timedelta(days=1))

class ScopeExpander(WindowScope):


    def shift(self):
        self.size += self.stride

    def inside(self):
        if self.start + self.size > self.max:
            return False
        return True


class ScopeRoller(WindowScope):


    def shift(self):
        self.start += self.stride

    def inside(self):
        if self.start > self.max:
            return False
        return True


class EnumScope(Scope):

    default_parameters = {'col': 'League', 'enum': ['GER1']}
    cur_index = 0

    def __init__(self, wrapper=None, parameters=default_parameters):
        super().__init__(wrapper, parameters)

    def set_parameters_from_wrapper(self, wrapper:DataWrapper):
        if 'enum' not in self.parameters:
            self.enum = pd.unique(self.wrapper.get_columns(self.col)).tolist()

    def shift(self):
        self.cur_index+=1

    def inside(self):
        if self.cur_index >= len(self.enum):
            return False
        return True

    def reset_state(self):
        self.cur_index = 0

    def current_state(self):
        return (self.col, [self.enum[self.cur_index]])
class TestingWindowScope(WindowScope):

    name = 'testing_window_scope'
    init_parameters = {name: {'col': 'Season', 'size': 1}}

    def __init__(self, training_window_scope: WindowScope, parameters = init_parameters, **kwargs) -> None:
        self.training_window_scope = training_window_scope
        super().__init__(parameters=parameters, **kwargs)

    def set_parameters(self, parameters):
        # calls super of WindowScope so it skips its implementation of set_parameters method
        if parameters is not None:
            self.start = self.training_window_scope.start + self.training_window_scope.size + 1
            self.max = self.training_window_scope.max
            self.stride = self.training_window_scope.stride
            self.orig_start = self.start
            self.orig_size = self.size