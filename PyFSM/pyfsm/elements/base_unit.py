import abc

from .event_type import EventType
from pyfsm.utils.list_utils import ListUtils


class BaseUnit(object):
    def __init__(self):
        self.name = None

    def __repr__(self):
        if self.name:
            return f'<Unit(name={self.name})>'
        else:
            return object.__repr__(self)


class VertexUnit(BaseUnit, metaclass=abc.ABCMeta):
    def __init__(self):
        BaseUnit.__init__(self)
        self.pseudo_unit = False

    @abc.abstractmethod
    def enter(self, event):
        pass

    @abc.abstractmethod
    def exit(self, event):
        pass

    @staticmethod
    def find_vertex_unit_from_sources(event, force=False):
        vertex_units = []
        if event.event_type == EventType.EXTERNAL or force:
            sources = ListUtils.get_or_else(event.sources)
            while True:
                sources_alt = []
                for source in sources:
                    if issubclass(type(source.unit), VertexUnit) and not source.unit.pseudo_unit:
                        vertex_units.append(source.unit)
                    else:
                        sources_alt += ListUtils.get_or_else(source.sources)
                if not sources_alt:
                    break
                sources = sources_alt
        return vertex_units


class VertexUnitAdapter(VertexUnit):
    def __init__(self):
        VertexUnit.__init__(self)

    def enter(self, event):
        pass

    def exit(self, event):
        pass

