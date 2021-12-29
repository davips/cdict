#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the cdict project.
#  Please respect the license - more about this in the section (*) below.
#
#  cdict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  cdict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with cdict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and it is unethical regarding the effort and
#  time spent here.
#
import operator
from functools import reduce
from itertools import chain
from typing import Union

from hosh import Hosh

from cdict.identification import f2hosh
from cdict.value.ival import iVal


class LazyiVal(iVal):
    """
    Identified lazy value

    Threefold lazy: It is calculated only when needed, only once and it is cached.

    >>> cache = {}
    >>> from cdict.value.strictival import StrictiVal
    >>> deps = {"x": StrictiVal(2)}
    >>> lvx = LazyiVal(lambda x: x**2, 0, 1, deps, [], cache=cache)
    >>> lvx
    →(x)
    >>> deps = {"x": lvx, "y": StrictiVal(3)}
    >>> result = []
    >>> f = lambda x,y: [x+y, y**2]
    >>> lvy = LazyiVal(f, 0, 2, deps, result, cache=cache)
    >>> lvz = LazyiVal(f, 1, 2, deps, result, cache=cache)
    >>> lvx, lvy, lvz
    (→(x), →(x→(x) y), →(x→(x) y))
    >>> deps = {"z": lvz}
    >>> f = lambda z: {"z":z**3, "w":z**5}
    >>> result = []
    >>> lvz2 = LazyiVal(f, 0, 2, deps, result, cache=cache)
    >>> lvw = LazyiVal(f, 1, 2, deps, result, cache=cache)
    >>> lvx, lvy, lvz2, lvw
    (→(x), →(x→(x) y), →(z→(x→(x) y)), →(z→(x→(x) y)))
    >>> lvx.value, lvy.value, lvz2.value, lvw.value
    (4, 7, 729, 59049)
    >>> lvz2.id
    'aILoOUz5h.C9f1xG8XB09cdEI0XwRBcX-o8IwxS7'
    >>> lvw.id
    'vG9pcVdnghFMbi26bsfiyI-C5BCzSoi-mfEgpOjz'
    >>> lvz2.hosh * lvw.hosh == lvz.hosh * lvw.fhosh
    True
    """

    def __init__(self, f: callable, i: int, n: int, deps: dict, result: list, fid: Union[str, Hosh] = None, cache=None):
        self.f = f
        self.i = i
        self.n = n
        self.deps = {} if deps is None else deps
        self.result = result
        self.fhosh = f2hosh(f) if fid is None else self.handle_id(fid)
        self.cache = {} if cache is None else cache
        self.hosh = reduce(operator.mul, chain(self.deps.values(), [self.fhosh]))[i:n]

    @property
    def value(self):
        if not self.result:
            deps = {}
            for field, ival in self.deps.items():
                deps[field] = ival.value
            result = self.f(**deps)
            if self.n == 1:
                result = [result]
            elif isinstance(result, dict):
                result = result.values()
            elif isinstance(result, list) and len(result) != self.n:  # pragma: no cover
                raise Exception(f"Wrong result length: {len(result)} differs from {self.n}")
            try:
                self.result.extend(result)
            except TypeError:  # pragma: no cover
                raise Exception(f"Unsupported multi-valued result type: {type(result)}")
        return self.result[self.i]

    def __repr__(self):
        if not self.result:
            return f"→({' '.join(k + ('' if dep.result else repr(dep)) for k, dep in self.deps.items())})"
        return repr(self.value)
