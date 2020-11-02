import abc

from ..elements import LinkElement


class TransitionBase(LinkElement, metaclass=abc.ABCMeta):
    pass
