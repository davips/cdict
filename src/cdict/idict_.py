from typing import Dict
from typing import TypeVar

VT = TypeVar("VT")


class Idict(Dict[str, VT]):
    """
    >>> for k in Idict(x=2):
    ...     print(k)
    x
    _id
    _ids
    >>> "x" in Idict(x=2)
    True
    """

    # noinspection PyMissingConstructor
    def __init__(self, /, _dictionary=None, _frozen=None, **kwargs):
        from cdict.frozenidict import FrozenIdict
        self.frozen = _frozen or FrozenIdict(_dictionary, **kwargs)

    def evaluate(self):
        """
        >>> from cdict.value import LazyiVal
        >>> d = Idict(x=LazyiVal(lambda: 2, 0, 1, {}, []))
        >>> d.show(colored=False)
        {
            "x": "→()",
            "_id": "Z9BHCaIxO5MXCxNFUjvaJI77y6C42LNh5HR4NrYM",
            "_ids": {
                "x": "oWSx.fifu6Srwe-008ixC8XVfZGqGzMpwS3cBOhv"
            }
        }
        >>> d.evaluate()
        >>> d.show(colored=False)
        {
            "x": "2",
            "_id": "Z9BHCaIxO5MXCxNFUjvaJI77y6C42LNh5HR4NrYM",
            "_ids": {
                "x": "oWSx.fifu6Srwe-008ixC8XVfZGqGzMpwS3cBOhv"
            }
        }
        """
        self.frozen.evaluate()

    @property
    def hosh(self):
        return self.frozen.hosh

    @property
    def id(self):
        """
        >>> from cdict import idict
        >>> idict(x=3, y=5, _z=5).id
        'ojflr9QKaLmxzQivMEss9hWVZfHpvihkPAYYd1da'
        """
        return self.hosh.id

    @property
    def ids(self):
        """
        >>> from cdict import idict
        >>> idict(x=3, y=5, _z=5).ids
        {'x': 'KGWjj0iyLAn1RG6RTGtsGE3omZraJM6xO.kvG5pr', 'y': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2', '_z': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2'}
        """
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
        _id 41wHsGFMSo0vbD2n6zAXogYG9YE3FwzIRSqjWc8N
        _ids {'x': 'DYu5bfVvb6FOhBCWNsss4wsEWHZYTbKnsVgoWFvl', 'y': 'k3PWYRxIEc0lEvD1f6rbnk.36RAD5AyfROy1aT29'}
        """
        return self.frozen.items(evaluate)

    @staticmethod
    def fromdict(dictionary, ids):
        """Build an idict from values and pre-defined ids

        >>> from hosh import Hosh
        >>> from cdict.value import StrictiVal
        >>> print(Idict.fromdict({"x": 3, "y": 5, "z": StrictiVal(7)}, ids={"x": Hosh(b"x"), "y": Hosh(b"y").id}))
        {"x": 3, "y": 5, "z": 7, "_id": "uf--zyyiojm5Tl.vFKALuyGhZRO0e0eH9irosr0i", "_ids": {"x": "ue7X2I7fd9j0mLl1GjgJ2btdX1QFnb1UAQNUbFGh", "y": "5yg5fDxFPxhEqzhoHgXpKyl5f078iBhd.pR0G2X0", "z": "eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf"}}
        """
        from cdict.frozenidict import FrozenIdict
        return Idict(_frozen=FrozenIdict.fromdict(dictionary, ids))

    @property
    def asdict(self):
        """
        >>> from cdict import idict
        >>> idict(x=3, y=5).asdict
        {'x': 3, 'y': 5, '_id': 'r5A2Mh6vRRO5rxi5nfXv1myeguGSTmqHuHev38qM', '_ids': {'x': 'KGWjj0iyLAn1RG6RTGtsGE3omZraJM6xO.kvG5pr', 'y': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2'}}
        """
        return self.frozen.asdict

    def astext(self, colored=True):
        r"""
        >>> from cdict import idict
        >>> repr(idict(x=3, y=5)) == idict(x=3, y=5).astext()
        True
        >>> print(repr(idict(x=3, y=5)))
        {
            "x": 3,
            "y": 5,
            "_id": "[38;5;225m[1m[48;5;0mr[0m[38;5;225m[1m[48;5;0m5[0m[38;5;15m[1m[48;5;0mA[0m[38;5;225m[1m[48;5;0m2[0m[38;5;225m[1m[48;5;0mM[0m[38;5;195m[1m[48;5;0mh[0m[38;5;225m[1m[48;5;0m6[0m[38;5;219m[1m[48;5;0mv[0m[38;5;183m[1m[48;5;0mR[0m[38;5;251m[1m[48;5;0mR[0m[38;5;177m[1m[48;5;0mO[0m[38;5;147m[1m[48;5;0m5[0m[38;5;183m[1m[48;5;0mr[0m[38;5;189m[1m[48;5;0mx[0m[38;5;15m[1m[48;5;0mi[0m[38;5;225m[1m[48;5;0m5[0m[38;5;225m[1m[48;5;0mn[0m[38;5;225m[1m[48;5;0mf[0m[38;5;15m[1m[48;5;0mX[0m[38;5;225m[1m[48;5;0mv[0m[38;5;225m[1m[48;5;0m1[0m[38;5;195m[1m[48;5;0mm[0m[38;5;225m[1m[48;5;0my[0m[38;5;219m[1m[48;5;0me[0m[38;5;183m[1m[48;5;0mg[0m[38;5;251m[1m[48;5;0mu[0m[38;5;177m[1m[48;5;0mG[0m[38;5;147m[1m[48;5;0mS[0m[38;5;183m[1m[48;5;0mT[0m[38;5;189m[1m[48;5;0mm[0m[38;5;15m[1m[48;5;0mq[0m[38;5;225m[1m[48;5;0mH[0m[38;5;225m[1m[48;5;0mu[0m[38;5;225m[1m[48;5;0mH[0m[38;5;15m[1m[48;5;0me[0m[38;5;225m[1m[48;5;0mv[0m[38;5;225m[1m[48;5;0m3[0m[38;5;195m[1m[48;5;0m8[0m[38;5;225m[1m[48;5;0mq[0m[38;5;219m[1m[48;5;0mM[0m",
            "_ids": {
                "x": "[38;5;239m[1m[48;5;0mK[0m[38;5;239m[1m[48;5;0mG[0m[38;5;60m[1m[48;5;0mW[0m[38;5;241m[1m[48;5;0mj[0m[38;5;97m[1m[48;5;0mj[0m[38;5;65m[1m[48;5;0m0[0m[38;5;133m[1m[48;5;0mi[0m[38;5;65m[1m[48;5;0my[0m[38;5;97m[1m[48;5;0mL[0m[38;5;66m[1m[48;5;0mA[0m[38;5;132m[1m[48;5;0mn[0m[38;5;61m[1m[48;5;0m1[0m[38;5;66m[1m[48;5;0mR[0m[38;5;95m[1m[48;5;0mG[0m[38;5;95m[1m[48;5;0m6[0m[38;5;239m[1m[48;5;0mR[0m[38;5;239m[1m[48;5;0mT[0m[38;5;239m[1m[48;5;0mG[0m[38;5;60m[1m[48;5;0mt[0m[38;5;241m[1m[48;5;0ms[0m[38;5;97m[1m[48;5;0mG[0m[38;5;65m[1m[48;5;0mE[0m[38;5;133m[1m[48;5;0m3[0m[38;5;65m[1m[48;5;0mo[0m[38;5;97m[1m[48;5;0mm[0m[38;5;66m[1m[48;5;0mZ[0m[38;5;132m[1m[48;5;0mr[0m[38;5;61m[1m[48;5;0ma[0m[38;5;66m[1m[48;5;0mJ[0m[38;5;95m[1m[48;5;0mM[0m[38;5;95m[1m[48;5;0m6[0m[38;5;239m[1m[48;5;0mx[0m[38;5;239m[1m[48;5;0mO[0m[38;5;239m[1m[48;5;0m.[0m[38;5;60m[1m[48;5;0mk[0m[38;5;241m[1m[48;5;0mv[0m[38;5;97m[1m[48;5;0mG[0m[38;5;65m[1m[48;5;0m5[0m[38;5;133m[1m[48;5;0mp[0m[38;5;65m[1m[48;5;0mr[0m",
                "y": "[38;5;227m[1m[48;5;0me[0m[38;5;221m[1m[48;5;0mc[0m[38;5;209m[1m[48;5;0mv[0m[38;5;149m[1m[48;5;0mg[0m[38;5;221m[1m[48;5;0mo[0m[38;5;215m[1m[48;5;0m-[0m[38;5;185m[1m[48;5;0mC[0m[38;5;221m[1m[48;5;0mB[0m[38;5;216m[1m[48;5;0mP[0m[38;5;192m[1m[48;5;0mi[0m[38;5;227m[1m[48;5;0m7[0m[38;5;222m[1m[48;5;0mw[0m[38;5;191m[1m[48;5;0mR[0m[38;5;215m[1m[48;5;0mW[0m[38;5;180m[1m[48;5;0mI[0m[38;5;192m[1m[48;5;0mx[0m[38;5;227m[1m[48;5;0mN[0m[38;5;221m[1m[48;5;0mz[0m[38;5;209m[1m[48;5;0mu[0m[38;5;149m[1m[48;5;0mo[0m[38;5;221m[1m[48;5;0m1[0m[38;5;215m[1m[48;5;0mH[0m[38;5;185m[1m[48;5;0mg[0m[38;5;221m[1m[48;5;0mH[0m[38;5;216m[1m[48;5;0mQ[0m[38;5;192m[1m[48;5;0mC[0m[38;5;227m[1m[48;5;0mb[0m[38;5;222m[1m[48;5;0md[0m[38;5;191m[1m[48;5;0mv[0m[38;5;215m[1m[48;5;0mR[0m[38;5;180m[1m[48;5;0m0[0m[38;5;192m[1m[48;5;0m5[0m[38;5;227m[1m[48;5;0m8[0m[38;5;221m[1m[48;5;0mx[0m[38;5;209m[1m[48;5;0mi[0m[38;5;149m[1m[48;5;0m6[0m[38;5;221m[1m[48;5;0mz[0m[38;5;215m[1m[48;5;0mm[0m[38;5;185m[1m[48;5;0mr[0m[38;5;221m[1m[48;5;0m2[0m"
            }
        }
        """
        return self.frozen.astext(colored)

    def show(self, colored=True):
        r"""
        Textual representation of an idict object

        >>> from cdict import idict
        >>> from cdict.appearance import decolorize
        >>> d = idict(x=1,y=2)
        >>> d.show(colored=False)
        {
            "x": 1,
            "y": 2,
            "_id": "41wHsGFMSo0vbD2n6zAXogYG9YE3FwzIRSqjWc8N",
            "_ids": {
                "x": "DYu5bfVvb6FOhBCWNsss4wsEWHZYTbKnsVgoWFvl",
                "y": "k3PWYRxIEc0lEvD1f6rbnk.36RAD5AyfROy1aT29"
            }
        }
        """
        return self.frozen.show(colored)

    def __iter__(self):
        return iter(self.frozen)

    def __contains__(self, item):
        return item in self.frozen

    def __repr__(self):
        return repr(self.frozen)

    def __str__(self):
        return str(self.frozen)
