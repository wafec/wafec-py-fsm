from ..elements import StateUnit
from ..utils import ListUtils
from .state_base import StateBase
from .initial_state import InitialState
from ..exceptions import InvalidElementException


class Region(StateUnit):
    def __init__(self):
        StateUnit.__init__(self)

    def add_state(self, states):
        for state in ListUtils.to_list(states):
            if isinstance(state, StateBase) and not isinstance(state, InitialState):
                self.children = ListUtils.add_or_create(self.children, state)
                state.levelers = self.starters
                state.parent = self
            else:
                raise InvalidElementException()

    def set_initial_state(self, initial_state):
        if isinstance(initial_state, InitialState):
            initial_state.parent = self
            self.starters = [initial_state]
            self.children = ListUtils.add_or_create(self.children, initial_state)
            for child in [child for child in self.children if child != initial_state]:
                child.starters = self.starters
