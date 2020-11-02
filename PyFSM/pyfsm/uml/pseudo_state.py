from .state_base import StateBase


class PseudoState(StateBase):
    def __init__(self):
        StateBase.__init__(self)
        self.pseudo_unit = True

    def increment_active_count_backward(self, increment_value):
        pass

    def increment_active_count(self, increment_value):
        pass
