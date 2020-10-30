from .base_unit import BaseUnit
from ..utils import ListUtils
from .transport_event import TransportEvent


class LinkElement(BaseUnit):
    def __init__(self):
        BaseUnit.__init__(self)
        self.sources = None
        self.destinations = None
        self.guards = None
        self.accepts = None

    def add_source(self, source):
        self.sources = ListUtils.add_or_create(self.sources, source)

    def add_destination(self, destination):
        self.destinations = ListUtils.add_or_create(self.destinations, destination)

    def add_guard(self, guard):
        self.guards = ListUtils.add_or_create(self.guards, guard)

    def add_accept(self, accept):
        self.accepts = ListUtils.add_or_create(self.accepts, accept)

    def accept(self, event):
        self_event = TransportEvent.of(event, self)
        if ListUtils.is_empty_or_any(self.accepts, self_event.id) and\
                ListUtils.is_empty_or_any_expr(self.guards, lambda guard: guard(self_event)):
            for destination in self.destinations:
                destination.accept(self_event)
