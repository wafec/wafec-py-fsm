from .transition_base import TransitionBase
from .state_base import StateBase
from ..utils import ListUtils
from ..exceptions import InvalidElementException


class Transition(TransitionBase):
    def __init__(self):
        TransitionBase.__init__(self)

    def add_destination(self, destinations):
        for destination in ListUtils.to_list(destinations):
            if isinstance(destination, StateBase):
                self.destinations = ListUtils.add_or_create(self.destinations, destination)
                destination.incoming = ListUtils.add_or_create(destination.incoming, self)
            else:
                raise InvalidElementException()

    def add_guard(self, guards):
        for guard in ListUtils.to_list(guards):
            if callable(guard):
                self.guards = ListUtils.add_or_create(self.guards, guard)
            else:
                raise InvalidElementException()

    def add_event(self, events):
        for event in ListUtils.to_list(events):
            self.accepts = ListUtils.add_or_create(self.accepts, event)

    @staticmethod
    def of(events, sources, destinations):
        transition = Transition()
        transition.add_event(events)
        for source in ListUtils.to_list(sources):
            source.add_transition(transition)
        transition.add_destination(destinations)
        return transition
