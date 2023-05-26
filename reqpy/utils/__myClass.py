"""
ALL CLASSES DEFINED FOR DRAGONFLY
"""

# ===============================  PROTECTED CLASS  =========================
from typing import Any


class ImmutableClass:
    '''Freeze any class such that instantiated
    objects become immutable. Also use __slots__ for speed.

    see: https://medium.datadriveninvestor.com/immutability-in-python-d57a3b23f336 # noqa: E501

    '''
    __slots__ = []  # type: ignore
    _frozen: bool = False

    def __init__(self):
        """generate __slots__ list dynamically"""
        for attr_name in dir(self):
            self.__slots__.append(attr_name)  # type: ignore
        self._frozen = True

    def __delattr__(self, *args: Any, **kwargs: Any):
        if self._frozen:
            raise AttributeError('This object is not mutable')
        object.__delattr__(self, *args, **kwargs)

    def __setattr__(self, *args: Any, **kwargs: Any):
        if self._frozen:
            raise AttributeError('This object is not mutable')
        object.__setattr__(self, *args, **kwargs)
