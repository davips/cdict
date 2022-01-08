import json
from collections import UserDict
from functools import cached_property
from typing import Dict, Union
from typing import TypeVar

from cdict.customjson import CustomJSONEncoder
from cdict.let import Let
from cdict.value import LazyiVal
from cdict.value.strictival import iVal, StrictiVal
from hosh import ø

VT = TypeVar("VT")


class FrozenIdict(UserDict, Dict[str, VT]):
    """
    Frozen version of Idict

    Nested idicts become frozen for consistent identities.

    >>> "x" in FrozenIdict(x=2)
    True
    """

    # noinspection PyMissingConstructor
    def __init__(self, /, _dictionary=None, **kwargs):
        from cdict.idict_ import Idict
        data: Dict[str, Union[iVal, str, dict]] = _dictionary or {}
        data.update(kwargs)
        if "_id" in data.keys() or "_ids" in data.keys():  # pragma: no cover
            raise Exception("Cannot have a field named '_id'/'_ids': {data.keys()}")
        self.data: Dict[str, Union[iVal, str, dict]] = {}
        self.hosh = ø
        self.ids = {}
        for k, v in data.items():
            if isinstance(v, iVal):
                self.data[k] = v
            else:
                self.data[k] = StrictiVal(v.frozen, v.hosh) if isinstance(v, Idict) else StrictiVal(v)
            self.hosh += self.data[k].hosh * k.encode()
            self.ids[k] = self.data[k].hosh.id
        # noinspection PyTypeChecker
        self.data["_id"] = self.id = self.hosh.id
        self.data["_ids"] = self.ids

    def evaluate(self):
        for k, ival in self.data.items():
            if k not in ["_id", "_ids"]:
                ival.evaluate()

    @cached_property
    def fields(self):
        """List of keys which don't start with '_'"""
        return [k for k in self.data if not k.startswith("_")]

    @cached_property
    def metafields(self):
        """List of keys which start with '_'"""
        return [k for k in self.data if k.startswith("_") and k not in ["_id", "_ids"]]

    @staticmethod
    def fromdict(dictionary, ids):
        """Build a frozenidict from values and pre-defined ids"""
        data = {}
        for k, v in dictionary.items():
            if isinstance(v, iVal):
                if k in ids:  # pragma: no cover
                    raise Exception(f"Conflict: key '{k}' provided for an iVal")
                data[k] = v
            else:
                data[k] = StrictiVal(v, ids[k])
        return FrozenIdict(data)

    @cached_property
    def asdict(self):
        dic = {k: v for k, v in self.entries()}
        dic["_id"] = self.id
        dic["_ids"] = self.ids.copy()
        return dic

    def astext(self, colored=True):
        r"""Textual representation of a frozenidict object"""
        txt = json.dumps(self.data, indent=4, ensure_ascii=False, cls=CustomJSONEncoder)

        # Put colors after json, to avoid escaping ansi codes.
        if colored:
            txt = txt.replace(self.data["_id"], self.hosh.ansi)
            for k, v in self.entries(evaluate=False):
                txt = txt.replace(v.id, v.hosh.idc)

        return txt

    def show(self, colored=True):
        r"""Print textual representation of a frozenidict object"""
        print(self.astext(colored))

    def items(self, evaluate=True):
        """Iterator over all items"""
        yield from self.entries(evaluate)
        yield "_id", self.id
        yield "_ids", self.ids

    def entries(self, evaluate=True):
        """Iterator over entries"""
        for k, ival in self.data.items():
            if k not in ["_id", "_ids"]:
                yield k, (ival.value if evaluate else ival)

    def copy(self):  # pragma: no cover
        raise Exception("A FrozenIdict doesn't need copies")

    @property
    def unfrozen(self):
        from cdict.idict_ import Idict
        return Idict(_frozen=self)

    def __setitem__(self, key: str, value):  # pragma: no cover
        print(value)
        raise Exception(f"Cannot set an entry ({key}) of a frozen dict.")

    def __delitem__(self, key):  # pragma: no cover
        raise Exception(f"Cannot delete an entry ({key}) from a frozen dict.")

    def __repr__(self):
        return self.astext()

    def __str__(self):
        return json.dumps(self.data, ensure_ascii=False, cls=CustomJSONEncoder)

    def __getitem__(self, item):
        return self.data[item] if item in ["_id", "_ids"] else self.data[item].value

    def __getattr__(self, item):  # pragma: no cover
        if item in self.data:
            return self.data[item].value
        return AttributeError

    def __rshift__(self, other):
        data = self.data.copy()
        del data["_id"]
        del data["_ids"]
        if isinstance(other, list):
            caches = []
            for cache in other:
                if isinstance(cache, list):
                    if len(cache) == 0:  # pragma: no cover
                        raise Exception("Missing content inside list for caching.")
                    elif len(cache) > 1:  # pragma: no cover
                        raise Exception(f"Cannot have more than one cache within a nested list: {cache} in {other}.")
                    self.evaluate()
                    cache = cache[0]
                caches.append(cache)
            nolazies = True
            for k, ival in self.entries(evaluate=False):
                if not ival.result:
                    nolazies = False
                    data[k] = ival.withcaches(caches)
            # Eager saving when there are no lazies.
            if nolazies:
                pass  # TODO
            return FrozenIdict(data)

        if isinstance(other, Let):
            n = len(other.output)
            deps = {}
            for fin_source, fin_target in other.input.items():
                if fin_source in data:
                    val = data[fin_source]
                elif fin_source in other.input_space:  # TODO: rnd
                    val = other.rnd.choice(other.input_space[fin_source])
                elif fin_source in other.input_values:
                    val = other.input_values[fin_source]
                else:  # pragma: no cover
                    raise Exception(f"Missing field '{fin_source}': {other.input}")
                deps[fin_target] = val
            shared_result = {}
            for i, fout in enumerate(other.output):
                data[fout] = LazyiVal(other.f, i, n, deps, shared_result, fid=other.id)
            return FrozenIdict(data)
        return NotImplemented
