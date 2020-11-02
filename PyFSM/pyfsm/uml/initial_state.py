from .pseudo_state import PseudoState


class InitialState(PseudoState):
    def __init__(self):
        PseudoState.__init__(self)

    def accept(self, event):
        self.receive(event)

    def enter(self, event):
        self.accept(event)
