from .pseudo_state import PseudoState
from ..utils import ListUtils
from ..elements import TransportEvent
from ..elements import VertexUnit


class Join(PseudoState):
    def __init__(self):
        PseudoState.__init__(self)
        self.incoming_count = 0

    def accept(self, event):
        self_event = TransportEvent.of(event, self)
        self.incoming_count += 1
        if self.incoming_count >= ListUtils.len_or_abs(self.incoming):
            self.incoming_count = 0
            self.receive(self_event)
        else:
            exit_units = VertexUnit.find_vertex_unit_from_sources(self_event)
            for exit_unit in exit_units:
                exit_unit.increment_active_count_backward(-1)
            for exit_unit in exit_units:
                exit_unit.exit()

