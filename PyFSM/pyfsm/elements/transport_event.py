from .base_unit import BaseUnit


class TransportEvent(BaseUnit):
    def __init__(self):
        self.sources = None
        self.destinations = None
        self.id = None
        self.data = None
