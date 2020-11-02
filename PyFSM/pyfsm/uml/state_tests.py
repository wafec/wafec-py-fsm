import unittest

from .state import State
from .region import Region
from .initial_state import InitialState
from .transition import Transition
from .join import Join
from .event import Event


class StateTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_state_with_region(self):
        state = State()
        region = Region()
        state.name = 'state1'
        region.name = 'region1'
        state.add_region(region)
        self.assertListEqual([region], state.children)
        self.assertListEqual([region], state.starters)
        self.assertEqual(state, region.parent)
        self.assertListEqual([region], region.levelers)

    def test_composite_state(self):
        state = State()
        region = Region()
        initial = InitialState()
        sub1 = State()
        sub2 = State()
        state.name = 'state'
        region.name = 'region'
        initial.name = 'initial'
        sub1.name = 'sub1'
        sub2.name = 'sub2'
        state.add_region(region)
        region.set_initial_state(initial)
        region.add_state([sub1, sub2])
        self.assertListEqual([initial], sub1.levelers)
        self.assertListEqual([initial], sub2.levelers)
        self.assertEqual(region, sub1.parent)
        self.assertEqual(region, sub2.parent)
        self.assertEqual(region, initial.parent)
        self.assertListEqual([initial, sub1, sub2], region.children)

    def test_transition(self):
        state1 = State()
        state2 = State()
        transition = Transition()
        state1.name = 'state1'
        state2.name = 'state2'
        transition.name = 'transition1_2'
        state1.add_transition(transition)
        transition.add_destination(state2)
        self.assertListEqual([state1], transition.sources)
        self.assertListEqual([state2], transition.destinations)
        self.assertListEqual([transition], state1.links)
        self.assertListEqual([transition], state2.incoming)

    def test_transition_when_created_through_factory(self):
        state1 = State()
        state2 = State()
        transition = Transition.of('event1', state1, state2)
        self.assertListEqual([transition], state1.links)
        self.assertListEqual([transition], state2.incoming)
        self.assertListEqual(['event1'], transition.accepts)

    def test_composite_state_count(self):
        state1 = State()
        state1.name = 'state1'
        region1 = Region()
        region1.name = 'region1'
        initial1 = InitialState()
        initial1.name = 'initial1'
        state1.add_region(region1)
        region1.set_initial_state(initial1)
        state2 = State()
        state2.name = 'state2'
        region1.add_state([state2])
        transition1 = Transition.of([None], initial1, state2)
        transition1.name = 'transition1'
        event = Event()
        event.id = None
        state1.initialize(event)


class StateMachineTests(unittest.TestCase):
    def setUp(self):
        self.state_machine = State()
        self.region1 = Region()
        self.region2 = Region()
        self.initial1 = InitialState()
        self.initial2 = InitialState()
        self.state_machine.name = 'state_machine'
        self.region1.name = 'region1'
        self.region2.name = 'region2'
        self.initial1.name = 'initial1'
        self.initial2.name = 'initial2'
        self.state_machine.add_region([self.region1, self.region2])
        self.region1.set_initial_state(self.initial1)
        self.region2.set_initial_state(self.initial2)
        self.state1_1 = State()
        self.state1_2 = State()
        self.state1_3 = State()
        self.region1.add_state([self.state1_1, self.state1_2, self.state1_3])
        self.state2_1 = State()
        self.state2_2 = State()
        self.state2_3 = State()
        self.region2.add_state([self.state2_1, self.state2_2, self.state2_3])
        self.state1_1.name = 'state1_1'
        self.state1_2.name = 'state1_2'
        self.state1_3.name = 'state1_3'
        self.state2_1.name = 'state2_1'
        self.state2_2.name = 'state2_2'
        self.state2_3.name = 'state2_3'
        self.join1_1 = Join()
        self.transition1_j1 = Transition.of([None], self.initial1, self.join1_1)
        self.transition1_1 = Transition.of([None], self.join1_1, self.state1_1)
        self.transition1_2 = Transition.of([None], self.join1_1, self.state1_2)
        self.join1_2 = Join()
        self.transition1_1_j2 = Transition.of('event3', self.state1_1, self.join1_2)
        self.transition1_2_j2 = Transition.of('event4', self.state1_2, self.join1_2)

    def test_hello(self):
        event = Event()
        event.id = 'event'
        self.state_machine.initialize(event)
        self.assertTrue(self.state1_1.active)
        self.assertTrue(self.state1_2.active)
        self.assertTrue(self.state_machine.active)
        self.assertTrue(self.region1.active)
        self.assertEqual(5, self.state_machine._active_count)
        self.assertEqual(3, self.region1._active_count)
        self.assertEqual(1, self.state1_1._active_count)