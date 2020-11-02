from .state_base import StateBase
from .region import Region
from ..utils import ListUtils
from ..exceptions import InvalidElementException


class State(StateBase):
    def __init__(self):
        StateBase.__init__(self)

    def add_region(self, regions):
        for region in ListUtils.to_list(regions):
            if isinstance(region, Region):
                self.children = ListUtils.add_or_create(self.children, region)
                region.parent = self
                self.starters = ListUtils.add_or_create(self.starters, region)
                region.levelers = [region]
            else:
                raise InvalidElementException()
