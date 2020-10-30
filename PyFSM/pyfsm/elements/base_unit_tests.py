import unittest

from pyfsm.elements import *


class VertexUnitTests(unittest.TestCase):
    def setUp(self):
        self.vertex1 = VertexUnitAdapter()
        self.vertex2 = VertexUnitAdapter()
        self.event1 = TransportEvent()
        self.event1.unit = self.vertex1
        self.event2 = TransportEvent.of(self.event1, self.vertex2)

    def test_find_vertex_unit_from_sources(self):
        result = VertexUnit.find_vertex_unit_from_sources(self.event2)
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], self.vertex1)