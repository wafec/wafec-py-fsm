import unittest

from pyfsm.elements import *


class StateUnitSimpleFsmTests(unittest.TestCase):
    def setUp(self):
        self.fsm = StateUnit()
        self.state1 = StateUnit()
        self.state2 = StateUnit()
        self.link1 = LinkElement()
        self.fsm.starters = [self.state1]
        self.state1.parent = self.fsm
        self.state2.parent = self.fsm
        self.state1.levelers = [self.state1]
        self.state2.levelers = [self.state2]
        self.state1.links = [self.link1]
        self.link1.sources = [self.state1]
        self.link1.destinations = [self.state2]
        self.state3 = StateUnit()
        self.link2 = LinkElement()
        self.link2.sources = [self.state2]
        self.link2.destinations = [self.state3]
        self.state2.links = [self.link2]
        self.state3.parent = self.fsm
        self.state3.levelers = [self.state1]

        self.fsm.children = [self.state1, self.state2, self.state3]
        self.fsm.name = 'fsm'
        self.state1.name = 'state1'
        self.state2.name = 'state2'
        self.state3.name = 'state3'

    def test_fsm_with_enter(self):
        event = TransportEvent()
        event.id = 'test'
        self.fsm.initialize(event)
        self.assertTrue(self.state1.active)
        self.assertTrue(self.fsm.active)
        self.assertFalse(self.state2.active)

    def test_fsm_with_first_transition(self):
        event = TransportEvent()
        event.id = 'test'
        self.fsm.initialize(event)
        self.fsm.receive(event)
        self.assertTrue(self.fsm.active)
        self.assertTrue(self.state2.active)
        self.assertFalse(self.state1.active)

    def test_fsm_with_second_transition(self):
        event = TransportEvent()
        event.id = 'test'
        self.fsm.initialize(event)
        self.fsm.receive(event)
        self.fsm.receive(event)
        self.assertTrue(self.state3.active)
        self.assertFalse(self.state2.active)
        self.assertFalse(self.state1.active)
        self.assertTrue(self.fsm.active)

    def test_fsm_with_entry_action(self):
        count = 0

        def increment_count(args):
            nonlocal count
            count += 1
        event = TransportEvent()
        event.id = 'test'
        self.state1.entry_actions = [increment_count]
        self.fsm.initialize(event)
        self.fsm.receive(event)
        self.assertEqual(1, count)

    def test_fsm_with_entry_action_and_view(self):
        def change_view(args):
            args.event.view['test'] = 'value'
        event = TransportEvent()
        event.id = 'test'
        self.state1.entry_actions = [change_view]
        self.fsm.initialize(event)
        self.fsm.receive(event)
        self.assertEqual('value', event.view['test'])

    def test_fsm_with_entry_in_all_units(self):
        count = 0

        def increment_count(args):
            nonlocal count
            count += 1
        event = TransportEvent()
        event.id = 'test'
        self.fsm.entry_actions = [increment_count]
        self.state1.entry_actions = [increment_count]
        self.state2.entry_actions = [increment_count]
        self.state3.entry_actions = [increment_count]
        self.fsm.initialize(event)
        self.fsm.receive(event)
        self.fsm.receive(event)
        self.assertEqual(4, count)

    def test_fsm_with_exit(self):
        count = 0

        def increment_count(args):
            nonlocal count
            count += 1
        self.state1.exit_actions = [increment_count]
        event = TransportEvent()
        event.id = 'test'
        self.fsm.initialize(event)
        self.fsm.receive(event)
        self.assertEqual(1, count)
        self.fsm.receive(event)
        self.assertEqual(1, count)

    def test_fsm_with_exit_and_entry(self):
        count = 0

        def increment_count(args):
            nonlocal count
            count += 1

        def decrement_count(args):
            nonlocal count
            count -= 1
        self.fsm.entry_actions = [increment_count]
        self.fsm.exit_actions = [decrement_count]
        self.state1.entry_actions = [increment_count]
        self.state1.exit_actions = [decrement_count]
        self.state2.entry_actions = [increment_count]
        self.state2.exit_actions = [decrement_count]
        self.state3.entry_actions = [increment_count]
        self.state3.exit_actions = [increment_count]
        event = TransportEvent()
        event.id = 'test'
        self.fsm.initialize(event)
        self.assertEqual(2, count)
        self.fsm.receive(event)
        self.assertEqual(2, count)
        self.fsm.receive(event)
        self.assertEqual(2, count)


class StateUnitComplexFsmTests(unittest.TestCase):
    def setUp(self):
        self.fsm = StateUnit()
        self.state10 = StateUnit()
        self.state20 = StateUnit()
        self.state11 = StateUnit()
        self.state12 = StateUnit()
        self.state21 = StateUnit()
        self.state22 = StateUnit()
        self.state23 = StateUnit()
        self.fsm.starters = [self.state10, self.state20]
        self.fsm.children = [self.state10, self.state11, self.state12, self.state20, self.state21, self.state22,
                             self.state23]
        self.state10.parent = self.fsm
        self.state11.parent = self.fsm
        self.state12.parent = self.fsm
        self.state20.parent = self.fsm
        self.state21.parent = self.fsm
        self.state22.parent = self.fsm
        self.state23.parent = self.fsm
        self.state10.levelers = [self.state10]
        self.state11.levelers = [self.state10]
        self.state12.levelers = [self.state10]
        self.state20.levelers = [self.state20]
        self.state21.levelers = [self.state20]
        self.state22.levelers = [self.state20]
        self.state23.levelers = [self.state20]
        self.link11 = LinkElement()
        self.link12 = LinkElement()
        self.link21 = LinkElement()
        self.link22 = LinkElement()
        self.link23 = LinkElement()
        self.link11.sources = [self.state10]
        self.link11.destinations = [self.state11]
        self.link12.sources = [self.state11]
        self.link12.destinations = [self.state12]
        self.link21 = LinkElement()
        self.link21.sources = [self.state20]
        self.link21.destinations = [self.state21]
        self.link22 = LinkElement()
        self.link22.sources = [self.state21]
        self.link22.destinations = [self.state22]
        self.link23 = LinkElement()
        self.link23.sources = [self.state22]
        self.link23.destinations = [self.state23]
        self.state10.links = [self.link11]
        self.state11.links = [self.link12]
        self.state20.links = [self.link21]
        self.state21.links = [self.link22]
        self.state22.links = [self.link23]
        self.link11.accepts = ['event11']
        self.link12.accepts = ['event11', 'event12']
        self.link21.accepts = ['event21']
        self.link22.accepts = ['event21', 'event22']
        self.link23.accepts = ['event21', 'event22', 'event23']
        self.event11 = TransportEvent()
        self.event12 = TransportEvent()
        self.event21 = TransportEvent()
        self.event22 = TransportEvent()
        self.event23 = TransportEvent()
        self.event0 = TransportEvent()
        self.event0.id = 'event0'
        self.event11.id = 'event11'
        self.event12.id = 'event12'
        self.event21.id = 'event21'
        self.event22.id = 'event22'
        self.event23.id = 'event23'

    def test_fsm_with_event(self):
        self.fsm.initialize(self.event0)
        self.assertTrue(self.fsm.active)
        self.assertTrue(self.state10.active)
        self.assertTrue(self.state20.active)
        self.assertFalse(self.state11.active)
        self.assertFalse(self.state21.active)
