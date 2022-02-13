#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the hoshmap project.
#  Please respect the license - more about this in the section (*) below.
#
#  hoshmap is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  hoshmap is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with hoshmap.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and it is unethical regarding the effort and
#  time spent here.
#
import operator
from functools import reduce
from typing import Union, Iterable

from hoshmap.identification import f2hosh
from hoshmap.value.ival import iVal
from hosh import Hosh
from itertools import chain


class LazyiVal(iVal):
    """
    Identified lazy value

    Threefold lazy: It is calculated only when needed, only once and it is cached.

    >>> cache = {}
    >>> from hoshmap.value.strictival import StrictiVal
    >>> deps = {"x": StrictiVal(2)}
    >>> lvx = LazyiVal(lambda x: x**2, 0, 1, deps, {}, caches=[cache])
    >>> lvx
    ←(x)
    >>> deps = {"x": lvx, "y": StrictiVal(3)}
    >>> result = {}
    >>> f = lambda x,y: [x+y, y**2]
    >>> lvy = LazyiVal(f, 0, 2, deps, result, caches=[cache])
    >>> lvz = LazyiVal(f, 1, 2, deps, result, caches=[cache])
    >>> lvx, lvy, lvz
    (←(x), ←(x←(x) y), ←(x←(x) y))
    >>> deps = {"z": lvz}
    >>> f = lambda z: {"z":z**3, "w":z**5}
    >>> result = {}
    >>> lvz2 = LazyiVal(f, 0, 2, deps, result, caches=[cache])
    >>> lvw = LazyiVal(f, 1, 2, deps, result, caches=[cache])
    >>> lvx, lvy, lvz2, lvw
    (←(x), ←(x←(x) y), ←(z←(x←(x) y)), ←(z←(x←(x) y)))
    >>> lvx.value, lvy.value, lvz2.value, lvw.value
    (4, 7, 729, 59049)
    >>> lvz2.id
    'aILoOUz5h.C9f1xG8XB09cdEI0XwRBcX-o8IwxS7'
    >>> lvw.id
    'vG9pcVdnghFMbi26bsfiyI-C5BCzSoi-mfEgpOjz'
    >>> lvz2.hosh * lvw.hosh == lvz.hosh * lvw.fhosh
    True
    """

    def __init__(self, f: callable, i: int, n: int, deps: dict, results: dict, fid: Union[str, Hosh] = None,
                 caches=None):
        # if i >= len(result):  # pragma: no cover
        #     raise Exception(f"Index {i} inconsistent with current expected result size {len(result)}.")
        self.f = f
        self.i = i
        self.n = n
        self.deps = {} if deps is None else deps
        self.result = results
        self.fhosh = f2hosh(f) if fid is None else self.handle_id(fid)
        self.caches = caches
        self.hosh = reduce(operator.mul, chain(self.deps.values(), [self.fhosh]))[i:n]
        self.result[self.id] = None

    def withcaches(self, caches):
        if self.caches is not None:  # pragma: no cover
            raise Exception("Caches already set.")
        return LazyiVal(self.f, self.i, self.n, self.deps, self.result, self.fhosh, caches)

    @property
    def value(self):
        if not self.evaluated:
            # Fetch.
            if self.caches is not None:
                outdated_caches = []
                for cache in self.caches:
                    if self.hosh.id in cache:
                        val = cache[self.hosh.id]
                        for outdated_cache in outdated_caches:
                            outdated_cache[self.hosh.id] = val
                        self.result[self.id] = val
                        return val
                    outdated_caches.append(cache)

            # Calculate.
            argnames = []
            kwargs = {}
            for field, ival in self.deps.items():
                if isinstance(field, int):
                    argnames.append(field)
                else:
                    kwargs[field] = ival.value
            result = self.f(*(self.deps[name] for name in sorted(argnames)), **kwargs)
            if self.n == 1:
                result = [result]
            elif isinstance(result, dict):
                result = result.values()
            elif isinstance(result, list) and len(result) != self.n:  # pragma: no cover
                raise Exception(f"Wrong result length: {len(result)} differs from {self.n}")
            if not isinstance(result, Iterable):  # pragma: no cover
                raise Exception(f"Unsupported multi-valued result type: {type(result)}")
            for id, res in zip(self.result, result):
                self.result[id] = res

            # Store.
            if self.caches is not None:
                for id, res in self.result.items():
                    for cache in self.caches:
                        cache[id] = res

        return self.result[self.id]

    def __repr__(self):
        if not self.evaluated:
            return f"←({' '.join(k + ('' if dep.evaluated else repr(dep)) for k, dep in self.deps.items())})"
        return repr(self.value)
