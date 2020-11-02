from .base_unit import BaseUnit
from ..utils import ListUtils
from .event_type import EventType


class TransportEvent(BaseUnit):
    def __init__(self):
        BaseUnit.__init__(self)
        self.sources = None
        self.destinations = None
        self.id = None
        self.data = None
        self.unit = None
        self.view = {}
        self.event_type = EventType.EXTERNAL

    def add_destination(self, destination):
        self.destinations = ListUtils.add_or_create(self.destinations, destination)

    def add_source(self, source):
        self.sources = ListUtils.add_or_create(self.sources, source)

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
        event.view = other.view
        event.event_type = other.event_type
        return event
