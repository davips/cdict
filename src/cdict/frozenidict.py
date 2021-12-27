import json
from collections import UserDict
from functools import cached_property
from typing import Dict
from typing import TypeVar

from hosh import ø

from cdict.value.customjson import CustomJSONEncoder
from cdict.value.strictival import iVal, StrictiVal

VT = TypeVar("VT")


class FrozenIdict(UserDict, Dict[str, VT]):
    # noinspection PyMissingConstructor
    def __init__(self, /, _dictionary=None, **kwargs):
        from cdict.idict_ import Idict
        data = _dictionary or {}
        data.update(kwargs)
        if "_id" in data.keys() or "_ids" in data.keys():  # pragma: no cover
            raise Exception("Cannot have a field named '_id'/'_ids': {data.keys()}")
        self.data = {}
        self.hosh = ø
        self.ids = {}
        for k, v in data.items():
            if isinstance(v, iVal):
                self.data[k] = v
            else:
                self.data[k] = StrictiVal(v, v.hosh) if isinstance(v, Idict) else StrictiVal(v)
            self.hosh *= self.data[k].hosh
            self.ids[k] = self.data[k].hosh.id
        self.data["_id"] = self.id = self.hosh.id
        self.data["_ids"] = self.ids

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

    def evaluate(self):
        for _, ival in self.entries():
            ival.evaluate()

    @property
    def asdict(self):
        dic = {k: v for k, v in self.entries()}
        dic["_id"] = self.id
        dic["_ids"] = self.ids.copy()
        return dic

    @property
    def astext(self):
        r"""Textual representation of a frozenidict object"""
        dic = {k: v for k, v in self.items(evaluate=False)}
        txt = json.dumps(dic, indent=4, ensure_ascii=False, cls=CustomJSONEncoder)

        # Put colors after json, to avoid escaping ansi codes.
        txt = txt.replace(dic["_id"], self.hosh.ansi)
        for k, v in self.entries(evaluate=False):
            txt = txt.replace(v.id, v.hosh.idc)
        return txt

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

    def __setitem__(self, key: str, value):  # pragma: no cover
        print(value)
        raise Exception(f"Cannot set an entry ({key}) of a frozen dict.")

    def __delitem__(self, key):  # pragma: no cover
        raise Exception(f"Cannot delete an entry ({key}) from a frozen dict.")

    def __repr__(self):
        return repr(self.data)
