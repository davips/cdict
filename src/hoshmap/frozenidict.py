import json
import re
from collections import UserDict
from functools import cached_property
from typing import Dict, Union
from typing import TypeVar

from hoshmap.serialization.customjson import CustomJSONEncoder
from hoshmap.let import Let
from hoshmap.value import LazyiVal
from hoshmap.value.dfival import DFiVal, explode_df
from hoshmap.value.strictival import iVal, StrictiVal
from hosh import ø

VT = TypeVar("VT")


class FrozenIdict(UserDict, Dict[str, VT]):
    """
    Frozen version of Idict

    Nested idicts become frozen for consistent identities.

    >>> "x" in FrozenIdict(x=2)
    True
    """

    _evaluated = None

    # noinspection PyMissingConstructor
    def __init__(self, /, _dictionary=None, **kwargs):
        from hoshmap.idict import Idict

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
                if isinstance(v, Idict):
                    self.data[k] = StrictiVal(v.frozen, v.hosh)
                elif str(type(v)) == "<class 'pandas.core.frame.DataFrame'>":
                    self.data[k], self.data[k + "_"] = explode_df(v)
                else:
                    self.data[k] = StrictiVal(v)
            if isinstance(k, str) and not k.startswith("_"):
                self.hosh += self.data[k].hosh * k.encode()
            self.ids[k] = self.data[k].hosh.id
        # noinspection PyTypeChecker
        self.data["_id"] = self.id = self.hosh.id
        self.data["_ids"] = self.ids

    @property
    def evaluated(self):
        if self._evaluated is None:
            self._evaluated = self.evaluate()
        return self

    def evaluate(self):
        for k, ival in self.data.items():
            if k not in ["_id", "_ids"]:
                ival.evaluate()
        return self

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

    def astext(self, colored=True, key_quotes=False):
        r"""Textual representation of a frozenidict object"""
        max = 0
        for k in self.fields:
            if len(k) > max:
                max = len(k)
        txt = json.dumps(self.data, indent=4, ensure_ascii=False, cls=CustomJSONEncoder)

        # Put colors after json, to avoid escaping ansi codes.
        if colored:
            txt = txt.replace(f'"{self.data["_id"]}"', self.hosh.ansi)
            for k, v in self.entries(evaluate=False):
                txt = txt.replace(f'"{v.id}"', v.hosh.idc)
        txt = re.sub(r'(": )"(λ.+?)"(?=,\n)', '": \\2', txt)
        if not key_quotes:
            txt = re.sub(r'(?<!: )"([a-zA-Z0-9_ ]+?)"(?=: )', '\\1', txt)
        return txt

    def show(self, colored=True, key_quotes=False):
        r"""Print textual representation of a frozenidict object"""
        print(self.astext(colored, key_quotes))

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
        from hoshmap.idict import Idict

        return Idict(_frozen=self)

    def __setitem__(self, key: str, value):  # pragma: no cover
        print(value)
        raise Exception(f"Cannot set an entry ({key}) of a frozen dict.")

    def __delitem__(self, key):  # pragma: no cover
        raise Exception(f"Cannot delete an entry ({key}) from a frozen dict.")

    def __repr__(self):
        return self.astext()

    def __str__(self):
        js = json.dumps(self.data, ensure_ascii=False, cls=CustomJSONEncoder)
        return re.sub(r'(?<!: )"(\S*?)"', '\\1', js)

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
        if isinstance(other, tuple):
            other = Let(other[0], other[1], *other[2:])
        from hoshmap.idict import Idict

        if isinstance(other, Idict):  # merge
            other = self.frozen
        if isinstance(other, FrozenIdict):  # merge
            other = other.data
        if isinstance(other, dict):  # merge
            for k, v in other.items():
                data[k] = v
            return FrozenIdict(data)
        # if not isinstance(other, list) and hasattr(other, "__setitem__") and hasattr(other, "__getitem__"):
        #     other = [other]
        if isinstance(other, list):
            caches = []
            strict = []
            for cache in other:
                if isinstance(cache, list):
                    cache = cache[0]
                    strict.append(cache)
                caches.append(cache)
                cache[self.id] = {"_ids": self.ids}
            for k, ival in self.entries(evaluate=False):
                if ival.isevaluated:
                    for cache in strict:
                        cache[ival.id] = ival.value  # TODO: pack (pickle+lz4)
                else:
                    data[k] = ival.withcaches(caches)
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
                    # TODO: partial application [put multiple references for same iPartial if multioutput]
                    #   raise exc if missing right most argument
                    raise Exception(f"Missing field '{fin_source}': {other.input}")
                if isinstance(val, iVal):
                    # REMINDER: only here 'val' comes from a field (not from Let)
                    deps[fin_target] = val
                elif str(type(val)) == "<class 'pandas.core.frame.DataFrame'>":
                    data[fin_target], data[fin_target + "_"] = explode_df(v)
                    deps[fin_target] = data[fin_target]
                else:
                    deps[fin_target] = StrictiVal(val)
            shared_result = {}
            for i, fout in enumerate(other.output):
                data[fout] = LazyiVal(other.f, i, n, deps, shared_result, fid=other.id)
            return FrozenIdict(data)
        return NotImplemented  # pragma: no cover

    def __eq__(self, other):
        if isinstance(other, dict):
            if "_id" in other:
                return self.id == other["_id"]
            if list(self.keys())[:-2] != list(other.keys()):
                return False
        if isinstance(other, dict):
            self.evaluate()
            data = self.asdict
            del data["_id"]
            del data["_ids"]
            return data == other
        raise TypeError(f"Cannot compare {type(self)} and {type(other)}")  # pragma: no cover

    def __ne__(self, other):
        return not (self == other)

    def __reduce__(self):
        return self.__class__, (self.data.copy(),)
