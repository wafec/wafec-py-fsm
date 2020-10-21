from .base_unit import BaseUnit


class StateUnit(BaseUnit):
    def __init__(self):
        self.initial = None
        self.links = None
        self.parent = None
        self.children = None
