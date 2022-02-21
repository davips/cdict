from typing import Dict, TypeVar

from hoshmap.let import Let

VT = TypeVar("VT")


# TODO: store functions (with reversed id)
# TODO:  DFiVal
# TODO: make storing of idict id->header flexible for new metafields/metavalues


class Idict(Dict[str, VT]):
    """
    >>> from hoshmap import _
    >>> d = _ >> {"x":2}
    >>> d.show(colored=False)
    {
        x: 2,
        _id: "v2D2UVaKRzSIbUr-4rxpRYs0y0ChtLz7qDkWlwJq",
        _ids: {
            x: "k3PWYRxIEc0lEvD1f6rbnk.36RAD5AyfROy1aT29"
        }
    }
    >>> for k in d:
    ...     print(k)
    x
    _id
    _ids
    >>> "x" in d
    True
    >>> f = lambda x: x**2
    >>> d >>= f, "->y"
    >>> d.show(colored=False)
    {
        x: 2,
        y: λ(x),
        _id: "FLGX7sHyzdwUh90DM.s41YTHOk4vz0Ie5kn6f9iI",
        _ids: {
            x: "k3PWYRxIEc0lEvD1f6rbnk.36RAD5AyfROy1aT29",
            y: "C4Y.SrjZPIH3rapdaSc-1BPQqyFHMHSVHqdbfCFg"
        }
    }
    >>> d.y, d["y"]
    (4, 4)
    >>> (d >> (lambda w: w**2, "y:w->y")).y
    16
    >>> (d >> (lambda w: w**2, "y:w→y")).y   # <AltGr + y> = →
    16
    >>> d == {"x": 2, "y": 4}
    True
    >>> _ >> {"x": 3} == {"x": 3}
    True
    >>> from hoshmap import idict
    >>> idict(x=3) == {"x": 3, "_id": idict(x=3).id}
    True
    >>> idict(x=3) == idict(x=3)
    True
    >>> idict(x=3).frozen == idict(x=3)
    True
    >>> idict(x=3) != {"x": 4}
    True
    >>> idict(x=3) != idict(x=4)
    True
    >>> idict(x=3).frozen != idict(x=4)
    True
    >>> idict(x=3) != {"y": 3}
    True
    >>> idict(x=3) != {"x": 3, "_id": (~idict(x=3).hosh).id}
    True
    >>> idict(x=3) != idict(y=3)
    True
    >>> d.show(colored=False)
    {
        x: 2,
        y: 4,
        _id: "FLGX7sHyzdwUh90DM.s41YTHOk4vz0Ie5kn6f9iI",
        _ids: {
            x: "k3PWYRxIEc0lEvD1f6rbnk.36RAD5AyfROy1aT29",
            y: "C4Y.SrjZPIH3rapdaSc-1BPQqyFHMHSVHqdbfCFg"
        }
    }
    >>> cache1 = {}
    >>> cache2 = {}
    >>> cache3 = {}
    >>> def f(x, y):
    ...     print("Evaluated!")
    ...     return x * y
    >>> d = idict(x=5, y=7) >> [[cache1]] >> (f, "x y→z") >> [cache2]
    >>> cache1, cache2
    ({'A0G3Y7KNMLihDvpSJ3tB.zxshc6u1CbbiiYjCAAA': {'_ids': {'x': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2', 'y': 'eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf'}}, 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2': 5, 'eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf': 7}, {})
    >>> d.show(colored=False)
    {
        x: 5,
        y: 7,
        z: λ(x y),
        _id: "KwLLDoyUJUh7atfP.6Ipy.WsFtAxjv6AecLRKZbF",
        _ids: {
            x: "ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2",
            y: "eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf",
            z: "ogZMm1I1npQj9FEidwVLX-2r4Tv5gqaVwDEgBTlD"
        }
    }
    >>> cache1, cache2
    ({'A0G3Y7KNMLihDvpSJ3tB.zxshc6u1CbbiiYjCAAA': {'_ids': {'x': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2', 'y': 'eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf'}}, 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2': 5, 'eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf': 7}, {})
    >>> d.z
    Evaluated!
    35
    >>> cache1, cache2, cache3
    ({'A0G3Y7KNMLihDvpSJ3tB.zxshc6u1CbbiiYjCAAA': {'_ids': {'x': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2', 'y': 'eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf'}}, 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2': 5, 'eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf': 7}, {'KwLLDoyUJUh7atfP.6Ipy.WsFtAxjv6AecLRKZbF': {'_ids': {'x': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2', 'y': 'eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf', 'z': 'ogZMm1I1npQj9FEidwVLX-2r4Tv5gqaVwDEgBTlD'}}, 'ogZMm1I1npQj9FEidwVLX-2r4Tv5gqaVwDEgBTlD': 35}, {})
    >>> e = idict(x=5, y=7) >> [cache1] >> (f, "x y→z") >> [cache3, cache2]
    >>> e.show(colored=False)
    {
        x: 5,
        y: 7,
        z: λ(x y),
        _id: "KwLLDoyUJUh7atfP.6Ipy.WsFtAxjv6AecLRKZbF",
        _ids: {
            x: "ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2",
            y: "eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf",
            z: "ogZMm1I1npQj9FEidwVLX-2r4Tv5gqaVwDEgBTlD"
        }
    }
    >>> e.z
    35
    >>> cache3
    {'KwLLDoyUJUh7atfP.6Ipy.WsFtAxjv6AecLRKZbF': {'_ids': {'x': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2', 'y': 'eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf', 'z': 'ogZMm1I1npQj9FEidwVLX-2r4Tv5gqaVwDEgBTlD'}}, 'ogZMm1I1npQj9FEidwVLX-2r4Tv5gqaVwDEgBTlD': 35}
    """

    # noinspection PyMissingConstructor
    def __init__(self, /, _dictionary=None, _frozen=None, **kwargs):
        from hoshmap.frozenidict import FrozenIdict

        self.frozen = _frozen or FrozenIdict(_dictionary, **kwargs)

    def __setitem__(self, key, value):
        self.frozen = self.frozen >> {key: value}

    def __delitem__(self, key):
        frozen = self.frozen.copy()
        del frozen[key]
        self.frozen = frozen

    def __getitem__(self, item):
        return self.frozen[item]

    def __getattr__(self, item):
        if item in self.frozen:
            return self.frozen[item]
        return self.__getattribute__(item)

    def __rshift__(self, other):
        if isinstance(other, (Let, list, dict, tuple)):
            return (self.frozen >> other).unfrozen
        return NotImplemented

    @property
    def evaluated(self):
        return self.frozen.evaluated

    def evaluate(self):
        """
        >>> from hoshmap.value import LazyiVal
        >>> d = Idict(x=LazyiVal(lambda: 2, 0, 1, {}, {}))
        >>> d.show(colored=False)
        {
            x: λ(),
            _id: "c26ifwYEjehRzg1eVGtB55BWIaCnYGmFF-R1WAaz",
            _ids: {
                x: "Uz80K1b-lTtVTq2axnaTpD3mD7PJAvlN4a49KXvh"
            }
        }
        >>> d.evaluate()
        >>> d.show(colored=False)
        {
            x: 2,
            _id: "c26ifwYEjehRzg1eVGtB55BWIaCnYGmFF-R1WAaz",
            _ids: {
                x: "Uz80K1b-lTtVTq2axnaTpD3mD7PJAvlN4a49KXvh"
            }
        }
        >>> d.evaluated.show(colored=False)
        {
            x: 2,
            _id: "c26ifwYEjehRzg1eVGtB55BWIaCnYGmFF-R1WAaz",
            _ids: {
                x: "Uz80K1b-lTtVTq2axnaTpD3mD7PJAvlN4a49KXvh"
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
        >>> from hoshmap import idict
        >>> idict(x=3, y=5, _z=5).id == idict(x=3, y=5).id
        True
        """
        return self.hosh.id

    @property
    def ids(self):
        """
        >>> from hoshmap import idict
        >>> idict(x=3, y=5, _z=5).ids
        {'x': 'KGWjj0iyLAn1RG6RTGtsGE3omZraJM6xO.kvG5pr', 'y': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2', '_z': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2'}
        """
        return self.frozen.ids

    @staticmethod
    def fromdict(dictionary, ids):
        """Build an idict from values and pre-defined ids

        >>> from hosh import Hosh
        >>> from hoshmap.value import StrictiVal
        >>> print(Idict.fromdict({"x": 3, "y": 5, "z": StrictiVal(7)}, ids={"x": Hosh(b"x"), "y": Hosh(b"y").id}))
        {x: 3, y: 5, z: 7, _id: "uf--zyyiojm5Tl.vFKALuyGhZRO0e0eH9irosr0i", _ids: {x: "ue7X2I7fd9j0mLl1GjgJ2btdX1QFnb1UAQNUbFGh", y: "5yg5fDxFPxhEqzhoHgXpKyl5f078iBhd.pR0G2X0", z: "eJCW9jGsdZTD6-AD9opKwjPIOWZ4R.T0CG2kdyzf"}}
        """
        from hoshmap.frozenidict import FrozenIdict

        return FrozenIdict.fromdict(dictionary, ids).unfrozen

    @property
    def asdict(self):
        """
        >>> from hoshmap import idict
        >>> idict(x=3, y=5).asdict
        {'x': 3, 'y': 5, '_id': 'r5A2Mh6vRRO5rxi5nfXv1myeguGSTmqHuHev38qM', '_ids': {'x': 'KGWjj0iyLAn1RG6RTGtsGE3omZraJM6xO.kvG5pr', 'y': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2'}}
        """
        return self.frozen.asdict

    @property
    def asdicts(self):
        """
        >>> from hoshmap import idict
        >>> idict(x=3, y=5).asdict
        {'x': 3, 'y': 5, '_id': 'r5A2Mh6vRRO5rxi5nfXv1myeguGSTmqHuHev38qM', '_ids': {'x': 'KGWjj0iyLAn1RG6RTGtsGE3omZraJM6xO.kvG5pr', 'y': 'ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2'}}
        """
        return self.frozen.asdicts

    def astext(self, colored=True, key_quotes=False):
        r"""
        >>> from hoshmap import idict
        >>> repr(idict(x=3, y=5)) == idict(x=3, y=5).astext()
        True
        >>> print(repr(idict(x=3, y=5)))
        {
            x: 3,
            y: 5,
            _id: [38;5;225m[1m[48;5;0mr[0m[38;5;225m[1m[48;5;0m5[0m[38;5;15m[1m[48;5;0mA[0m[38;5;225m[1m[48;5;0m2[0m[38;5;225m[1m[48;5;0mM[0m[38;5;195m[1m[48;5;0mh[0m[38;5;225m[1m[48;5;0m6[0m[38;5;219m[1m[48;5;0mv[0m[38;5;183m[1m[48;5;0mR[0m[38;5;251m[1m[48;5;0mR[0m[38;5;177m[1m[48;5;0mO[0m[38;5;147m[1m[48;5;0m5[0m[38;5;183m[1m[48;5;0mr[0m[38;5;189m[1m[48;5;0mx[0m[38;5;15m[1m[48;5;0mi[0m[38;5;225m[1m[48;5;0m5[0m[38;5;225m[1m[48;5;0mn[0m[38;5;225m[1m[48;5;0mf[0m[38;5;15m[1m[48;5;0mX[0m[38;5;225m[1m[48;5;0mv[0m[38;5;225m[1m[48;5;0m1[0m[38;5;195m[1m[48;5;0mm[0m[38;5;225m[1m[48;5;0my[0m[38;5;219m[1m[48;5;0me[0m[38;5;183m[1m[48;5;0mg[0m[38;5;251m[1m[48;5;0mu[0m[38;5;177m[1m[48;5;0mG[0m[38;5;147m[1m[48;5;0mS[0m[38;5;183m[1m[48;5;0mT[0m[38;5;189m[1m[48;5;0mm[0m[38;5;15m[1m[48;5;0mq[0m[38;5;225m[1m[48;5;0mH[0m[38;5;225m[1m[48;5;0mu[0m[38;5;225m[1m[48;5;0mH[0m[38;5;15m[1m[48;5;0me[0m[38;5;225m[1m[48;5;0mv[0m[38;5;225m[1m[48;5;0m3[0m[38;5;195m[1m[48;5;0m8[0m[38;5;225m[1m[48;5;0mq[0m[38;5;219m[1m[48;5;0mM[0m,
            _ids: {
                x: [38;5;239m[1m[48;5;0mK[0m[38;5;239m[1m[48;5;0mG[0m[38;5;60m[1m[48;5;0mW[0m[38;5;241m[1m[48;5;0mj[0m[38;5;97m[1m[48;5;0mj[0m[38;5;65m[1m[48;5;0m0[0m[38;5;133m[1m[48;5;0mi[0m[38;5;65m[1m[48;5;0my[0m[38;5;97m[1m[48;5;0mL[0m[38;5;66m[1m[48;5;0mA[0m[38;5;132m[1m[48;5;0mn[0m[38;5;61m[1m[48;5;0m1[0m[38;5;66m[1m[48;5;0mR[0m[38;5;95m[1m[48;5;0mG[0m[38;5;95m[1m[48;5;0m6[0m[38;5;239m[1m[48;5;0mR[0m[38;5;239m[1m[48;5;0mT[0m[38;5;239m[1m[48;5;0mG[0m[38;5;60m[1m[48;5;0mt[0m[38;5;241m[1m[48;5;0ms[0m[38;5;97m[1m[48;5;0mG[0m[38;5;65m[1m[48;5;0mE[0m[38;5;133m[1m[48;5;0m3[0m[38;5;65m[1m[48;5;0mo[0m[38;5;97m[1m[48;5;0mm[0m[38;5;66m[1m[48;5;0mZ[0m[38;5;132m[1m[48;5;0mr[0m[38;5;61m[1m[48;5;0ma[0m[38;5;66m[1m[48;5;0mJ[0m[38;5;95m[1m[48;5;0mM[0m[38;5;95m[1m[48;5;0m6[0m[38;5;239m[1m[48;5;0mx[0m[38;5;239m[1m[48;5;0mO[0m[38;5;239m[1m[48;5;0m.[0m[38;5;60m[1m[48;5;0mk[0m[38;5;241m[1m[48;5;0mv[0m[38;5;97m[1m[48;5;0mG[0m[38;5;65m[1m[48;5;0m5[0m[38;5;133m[1m[48;5;0mp[0m[38;5;65m[1m[48;5;0mr[0m,
                y: [38;5;227m[1m[48;5;0me[0m[38;5;221m[1m[48;5;0mc[0m[38;5;209m[1m[48;5;0mv[0m[38;5;149m[1m[48;5;0mg[0m[38;5;221m[1m[48;5;0mo[0m[38;5;215m[1m[48;5;0m-[0m[38;5;185m[1m[48;5;0mC[0m[38;5;221m[1m[48;5;0mB[0m[38;5;216m[1m[48;5;0mP[0m[38;5;192m[1m[48;5;0mi[0m[38;5;227m[1m[48;5;0m7[0m[38;5;222m[1m[48;5;0mw[0m[38;5;191m[1m[48;5;0mR[0m[38;5;215m[1m[48;5;0mW[0m[38;5;180m[1m[48;5;0mI[0m[38;5;192m[1m[48;5;0mx[0m[38;5;227m[1m[48;5;0mN[0m[38;5;221m[1m[48;5;0mz[0m[38;5;209m[1m[48;5;0mu[0m[38;5;149m[1m[48;5;0mo[0m[38;5;221m[1m[48;5;0m1[0m[38;5;215m[1m[48;5;0mH[0m[38;5;185m[1m[48;5;0mg[0m[38;5;221m[1m[48;5;0mH[0m[38;5;216m[1m[48;5;0mQ[0m[38;5;192m[1m[48;5;0mC[0m[38;5;227m[1m[48;5;0mb[0m[38;5;222m[1m[48;5;0md[0m[38;5;191m[1m[48;5;0mv[0m[38;5;215m[1m[48;5;0mR[0m[38;5;180m[1m[48;5;0m0[0m[38;5;192m[1m[48;5;0m5[0m[38;5;227m[1m[48;5;0m8[0m[38;5;221m[1m[48;5;0mx[0m[38;5;209m[1m[48;5;0mi[0m[38;5;149m[1m[48;5;0m6[0m[38;5;221m[1m[48;5;0mz[0m[38;5;215m[1m[48;5;0mm[0m[38;5;185m[1m[48;5;0mr[0m[38;5;221m[1m[48;5;0m2[0m
            }
        }
        """
        return self.frozen.astext(colored, key_quotes)

    def show(self, colored=True, key_quotes=False):
        r"""
        Textual representation of an idict object

        >>> from hoshmap import idict
        >>> from hoshmap.appearance import decolorize
        >>> d = idict(x=1,y=2)
        >>> d.show(colored=False)
        {
            x: 1,
            y: 2,
            _id: "41wHsGFMSo0vbD2n6zAXogYG9YE3FwzIRSqjWc8N",
            _ids: {
                x: "DYu5bfVvb6FOhBCWNsss4wsEWHZYTbKnsVgoWFvl",
                y: "k3PWYRxIEc0lEvD1f6rbnk.36RAD5AyfROy1aT29"
            }
        }
        """
        return self.frozen.show(colored, key_quotes)

    def __iter__(self):
        return iter(self.frozen)

    def __contains__(self, item):
        return item in self.frozen

    def __repr__(self):
        return repr(self.frozen)

    def __str__(self):
        return str(self.frozen)

    def __eq__(self, other):
        return self.frozen == other

    def __ne__(self, other):
        return not (self == other)

    def __reduce__(self):
        return self.frozen.__reduce__()

    def keys(self):
        """Generator of keys which don't start with '_'"""
        return self.frozen.keys()

    def values(self, evaluate=True):
        """Generator of field values (keys don't start with '_')"""
        return self.frozen.values(evaluate)

    def items(self, evaluate=True):
        """Generator over field-value pairs

        Include ids and other items starting with '_'.

        >>> from hoshmap import idict
        >>> from hoshmap.appearance import decolorize
        >>> for k, v in idict(x=1, y=2).items():
        ...     print(k, v)
        x 1
        y 2
        """
        return self.frozen.items(evaluate)

    def metakeys(self):
        """Generator of keys which start with '_'"""
        return self.frozen.metakeys()

    def metavalues(self, evaluate=True):
        """Generator of field values (keys don't start with '_')"""
        return self.frozen.metavalues(evaluate)

    def metaitems(self, evaluate=True):
        """Generator over field-value pairs"""
        return self.frozen.metaitems(evaluate)

    def entries(self, evaluate=True):
        """Iterator over all entries

        Ignore id entries.

        >>> from hoshmap import idict
        >>> from hoshmap.appearance import decolorize
        >>> for k, v in idict(x=1, y=2).entries():
        ...     print(k, v)
        x 1
        y 2
        """
        return self.frozen.entries(evaluate)

    @property
    def fields(self):
        """
        List of keys which don't start with '_'

        >>> from hoshmap import idict
        >>> idict(x=3, y=5, _z=5).fields
        ['x', 'y']
        """
        return self.frozen.fields

    @property
    def aslist(self):
        return self.frozen.aslist

    @property
    def metafields(self):
        """
        List of keys which don't start with '_'

        >>> from hoshmap import idict
        >>> idict(x=3, y=5, _z=5).metafields
        ['_z']
        """
        return self.frozen.metafields
