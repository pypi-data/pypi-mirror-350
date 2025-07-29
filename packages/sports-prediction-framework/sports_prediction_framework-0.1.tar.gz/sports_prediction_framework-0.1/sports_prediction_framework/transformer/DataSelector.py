from sports_prediction_framework.transformer.Scope import Scope
from sports_prediction_framework.transformer.ScopeSelector import *


class DataSelector:
    """
    Manages synchronized updates across training and testing data scopes.

    DataSelector coordinates iteration over combinations of training and testing
    scopes, applying logic such as updating, validation (`holds()`), and resetting
    of state. It serves as a unified interface to handle these paired scopes and
    traverse all valid combinations recursively, even when the number of scopes differs.

    Attributes:
        train_selectors (list[ScopeSelector]): List of training data scope selectors.
        test_selectors (list[ScopeSelector]): List of testing data scope selectors.
        max_index (int): The maximum number of selectors among train/test.
        selector_index (int): The current index of the selector being updated.
    """

    train_selectors = [Scope]
    test_selectors = [Scope]

    def __init__(self, train_selectors: [ScopeSelector] = [], test_selectors: [ScopeSelector] = [],
                 wrapper: DataWrapper = None):
        self.train_selectors = train_selectors
        self.test_selectors = test_selectors
        self.max_index = max(len(train_selectors), len(test_selectors))
        self.selector_index = self.max_index - 1


    def holds(self):
        if self.selector_index < 0 or (self.train_selectors and not self.train_selectors[0].holds()) or \
                (self.test_selectors and not self.test_selectors[0].holds()):
            return False
        return True

    def update(self):
        """
        Recursively updates training and testing scopes in a synchronized way.

        This method performs a backtracking traversal through all valid combinations
        of training and testing scopes, calling `update()` on each scope pair and
        ensuring both satisfy their `holds()` condition. If a combination fails, it
        resets the scopes and backtracks to try other possibilities.

        Handles cases where the number of training and testing scopes differs, enabling
        distinct granularity in data iteration.

        Iteration begins at the last scope and progresses through all valid configurations.
        """
        if not self.holds():
            return
        if self.selector_index == self.max_index:
            self.selector_index -= 1
        train_scope = None
        test_scope = None
        if self.selector_index < len(self.train_selectors):
            train_scope = self.train_selectors[self.selector_index]
            train_scope.update()
        if self.selector_index < len(self.test_selectors):
            test_scope = self.test_selectors[self.selector_index]
            test_scope.update()
        if (train_scope is None or train_scope.holds()) and (test_scope is None or test_scope.holds()):
            self.selector_index += 1
        else:
            if train_scope is not None:
                train_scope.reset_state()
            if test_scope is not None:
                test_scope.reset_state()
            self.selector_index -= 1
            self.update()


    def transform_wrapper(self, wrapper: DataWrapper, selectors: [ScopeSelector]):
        wrapper_trans = wrapper
        for selector in selectors:
            wrapper_trans = selector.transform(wrapper_trans)
# Used only for informative purposes. TO BE IMPLEMENTED or REMOVED
            #cur = selector.current_state()
            #wrapper_trans.current_selection[cur[0]] = cur[1]
        return wrapper_trans

    def transform_test(self, wrapper: DataWrapper):
        return self.transform_wrapper(wrapper, self.test_selectors)

    def transform_train(self, wrapper: DataWrapper):
        return self.transform_wrapper(wrapper, self.train_selectors)

    def reset_state(self):
        self.selector_index = self.max_index - 1
        for selector in self.train_selectors:
            selector.reset_state()
