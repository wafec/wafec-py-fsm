import abc

from ..elements import StateUnit
from .transition_base import TransitionBase
from ..exceptions import InvalidElementException
from ..utils import ListUtils


class StateBase(StateUnit, metaclass=abc.ABCMeta):
    def add_transition(self, transitions):
        for transition in ListUtils.to_list(transitions):
            if isinstance(transition, TransitionBase):
                self.links = ListUtils.add_or_create(self.links, transition)
                transition.sources = ListUtils.add_or_create(transition.sources, self)
            else:
                raise InvalidElementException()

    def set_entry_actions(self, entry_actions):
        self.entry_actions = None
        for entry_action in ListUtils.to_list(entry_actions):
            if callable(entry_action):
                self.entry_actions = ListUtils.add_or_create(self.entry_actions, entry_action)
            else:
                raise InvalidElementException()

    def set_exit_actions(self, exit_actions):
        self.exit_actions = None
        for exit_action in ListUtils.to_list(exit_actions):
            if callable(exit_action):
                self.exit_actions = ListUtils.add_or_create(self.exit_actions, exit_action)
            else:
                raise InvalidElementException()
