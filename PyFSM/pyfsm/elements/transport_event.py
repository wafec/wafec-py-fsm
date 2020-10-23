from .base_unit import BaseUnit
from ..utils import ListUtils


class TransportEvent(BaseUnit):
    def __init__(self):
        self.sources = None
        self.destinations = None
        self.id = None
        self.data = None
        self.unit = None

    def add_destination(self, destination):
        self.destinations = ListUtils.add_or_create(self.destinations, destination)

    def add_source(self, source):
        self.sources = ListUtils.add_or_create(self.sources)

    @staticmethod
    def of(other, unit):
        if unit == other.unit:
            return other
        event = TransportEvent()
        event.add_source(other)
        other.add_destination(event)
        event.id = other.id
        event.data = other.data
        event.unit = unit
        return event
