from .base_unit import VertexUnit
from .transport_event import TransportEvent
from ..utils import ListUtils
from .event_type import EventType


class StateUnit(VertexUnit):
    def __init__(self):
        VertexUnit.__init__(self)
        self.starters = None
        self.links = None
        self.parent = None
        self.levelers = None
        self.children = None
        self._active_count = 0
        self._active_flag = False
        self.locked = False
        self.exit_actions = None
        self.entry_actions = None
        self.incoming = None

    @property
    def active(self):
        return self.pseudo_unit or self._active_flag

    @property
    def _is_active(self):
        return self.pseudo_unit or self._active_count > 0

    def do_entry(self, event):
        for action in ListUtils.get_or_else(self.entry_actions):
            action(StateUnitEventArgs.of(self, event))

    def do_exit(self, event):
        for action in ListUtils.get_or_else(self.exit_actions):
            action(StateUnitEventArgs.of(self, event))

    def initialize(self, event):
        self.increment_active_count_backward(1)
        self.enter(event)

    def enter(self, event):
        self_event = TransportEvent.of(event, self)
        self_event.event_type = EventType.INTERNAL
        if self._is_active and not self._active_flag:
            self._active_flag = True
            if self.parent:
                self.parent.enter(self_event)
            self.do_entry(self_event)
            if self.starters:
                for starter in self.starters:
                    if not starter.locked:
                        starter.increment_active_count_backward(1)
                        starter.enter(self_event)

    def accept(self, event):
        self_event = TransportEvent.of(event, self)
        exit_units = VertexUnit.find_vertex_unit_from_sources(self_event)
        self.compute_active_count_before(exit_units)
        for exit_unit in exit_units:
            exit_unit.exit(event)
        self._lock_levelers(True)
        self.enter(self_event)
        self._lock_levelers(False)

    def increment_active_count_backward(self, increment_value):
        self.increment_active_count(increment_value)
        if self.parent:
            self.parent.increment_active_count_backward(increment_value)

    def increment_active_count(self, increment_value):
        self._active_count += increment_value

    def compute_active_count_before(self, exit_units):
        for exit_unit in exit_units:
            exit_unit.increment_active_count_backward(-1)
        self.increment_active_count_backward(1)

    def _lock_levelers(self, val=True):
        for leveler in ListUtils.get_or_else(self.levelers):
            leveler.locked = val

    def receive(self, event):
        if self._is_active:
            self_event = TransportEvent.of(event, self)
            if not self.pseudo_unit:
                self_event.event_type = EventType.EXTERNAL
            for child in [child for child in ListUtils.get_or_else(self.children) if child.active]:
                child.receive(self_event)
            for link in ListUtils.get_or_else(self.links):
                link.accept(self_event)

    def exit(self, event):
        if not self._is_active and self._active_flag:
            self._active_flag = False
            self_event = TransportEvent.of(event, self)
            for child in ListUtils.get_or_else(self.children):
                child.exit(self_event)
            self.do_exit(event)
            if self.parent:
                self.parent.exit(event)


class StateUnitEventArgs(object):
    def __init__(self, unit, event):
        self.unit = unit
        self.event = event

    @staticmethod
    def of(unit, event):
        return StateUnitEventArgs(unit, event)