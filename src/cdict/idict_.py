from collections import UserDict
from typing import Dict
from typing import TypeVar

VT = TypeVar("VT")


class Idict(UserDict, Dict[str, VT]):
    # noinspection PyMissingConstructor
    def __init__(self, /, _dictionary=None, _frozen=None, **kwargs):
        from cdict.frozenidict import FrozenIdict
        self.frozen = _frozen or FrozenIdict(_dictionary, **kwargs)

    @property
    def hosh(self):
        return self.frozen.hosh

    @property
    def id(self):
        return self.hosh.id

    @property
    def ids(self):
        return self.frozen.ids

    @property
    def fields(self):
        """
        List of keys which don't start with '_'

        >>> from cdict import idict
        >>> idict(x=3, y=5, _z=5).fields
        ['x', 'y']
        """
        return self.frozen.fields

    @property
    def metafields(self):
        """
        List of keys which don't start with '_'

        >>> from cdict import idict
        >>> idict(x=3, y=5, _z=5).metafields
        ['_z']
        """
        return self.frozen.metafields

    def entries(self, evaluate=True):
        """Iterator over entries

        Ignore id entries.

        >>> from cdict import idict
        >>> from cdict.appearance import decolorize
        >>> for k, v in idict(x=1, y=2).entries():
        ...     print(k, v)
        x 1
        y 2
        """
        return self.frozen.entries(evaluate)

    def items(self, evaluate=True):
        """Iterator over all items

        Include ids and other items starting with '_'.

        >>> from cdict import idict
        >>> from cdict.appearance import decolorize
        >>> for k, v in idict(x=1, y=2).items():
        ...     print(k, v)
        x 1
        y 2
        _id AWC3JzkHxmgMUMuFXgcu7UrpqHGAZLgDhIPp4xyu
        _ids {'x': 'DYu5bfVvb6FOhBCWNsss4wsEWHZYTbKnsVgoWFvl', 'y': 'k3PWYRxIEc0lEvD1f6rbnk.36RAD5AyfROy1aT29'}
        """
        return self.frozen.items(evaluate)

    @staticmethod
    def fromdict(dictionary, ids):
        """Build an idict from values and pre-defined ids

        >>> from hosh import Hosh
        >>> Idict.fromdict({"x": 3, "y": 5}, ids={"x": Hosh(b"x"), "y": Hosh(b"y").id})
        {'x': 3, 'y': 5, '_id': 'B52Iiu2b0xZtdO3tYchImat8qo7OFMi5AeDVRHBi', '_ids': {'x': 'ue7X2I7fd9j0mLl1GjgJ2btdX1QFnb1UAQNUbFGh', 'y': '5yg5fDxFPxhEqzhoHgXpKyl5f078iBhd.pR0G2X0'}}
        """
        from cdict.frozenidict import FrozenIdict
        return Idict(_frozen=FrozenIdict.fromdict(dictionary, ids))

    @property
    def asdict(self):
        """
        >>> from cdict import idict
        >>> idict(x=3, y=5).asdict
        {'x': 3, 'y': 5, '_id': 'hmvr39APuGj.iS8QsTdnozY6SwEncC7CWwDBdsQt', '_ids': {'x': 'KGWjj0iyLAn1RG6RTGtsGE3omZraJM6xO.kvG5pr', 'y': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2'}}
        """
        return self.frozen.asdict

    @property
    def astext(self):
        r"""
        Textual representation of an idict object

        >>> from cdict import idict
        >>> from cdict.appearance import decolorize
        >>> d = idict(x=1,y=2)
        >>> decolorize(d.astext)
        '{\n    "x": 1,\n    "y": 2,\n    "_id": "AWC3JzkHxmgMUMuFXgcu7UrpqHGAZLgDhIPp4xyu",\n    "_ids": {\n        "x": "DYu5bfVvb6FOhBCWNsss4wsEWHZYTbKnsVgoWFvl",\n        "y": "k3PWYRxIEc0lEvD1f6rbnk.36RAD5AyfROy1aT29"\n    }\n}'
        """
        return self.frozen.astext

    def __iter__(self):
        return iter(self.frozen)

    def __repr__(self):
        return repr(self.frozen)
