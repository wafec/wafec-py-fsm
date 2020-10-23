from .base_unit import BaseUnit
from .transport_event import TransportEvent
from ..utils import ListUtils


class StateUnit(BaseUnit):
    def __init__(self):
        self.starters = None
        self.links = None
        self.parent = None
        self.children = None

        self.active = False

    def do_entry(self, event):
        pass

    def enter(self, event):
        self_event = TransportEvent.of(event, self)
        if not self.active:
            self.do_entry(self_event)
            if self.starters:
                for starter in self.starters:
                    starter.enter(self_event)

    def accept(self, event):
        self_event = TransportEvent.of(event, self)
        self.enter(self_event)

    def receive(self, event):
        if self.active:
            self_event = TransportEvent.of(event, self)
            for child in ListUtils.get_or_else(self.children):
                child.receive(self_event)
            for link in ListUtils.get_or_else(self.links):
                link.accept(self_event)
