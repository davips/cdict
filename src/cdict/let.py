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
from inspect import signature
from typing import Union, Iterable

from hosh import Hosh


class Let:
    def __init__(self, f: callable, in_out: str, /, _id: Union[str, Hosh] = None, _metadata=None, **kwargs):
        if "->" not in in_out:  # pragma: no cover
            raise Exception(f"Missing '->' in in_out schema ({in_out}).")
        instr, outstr = in_out.split("->")
        if outstr == "":  # pragma: no cover
            raise Exception(f"Missing output field names after '->' in in_out schema ({in_out}).")
        self.f = f
        if instr == "":
            self.input = {par.name: par.name for par in signature(f).parameters.values()}
        else:
            self.input = {}
            self.input_space = {}
            self.input_values = {}
            for i in instr.split(","):
                if ":" in i:
                    ii = i.split(":")
                    if len(ii) != 2:   # pragma: no cover
                        raise Exception(f"Wrong number ({len(ii)}) of ':' chars: {ii}")
                    isource, itarget = ii
                else:
                    isource = itarget = i
                if isource.startswith("~"):
                    isource = isource[1:]
                    if isource not in kwargs or isinstance(kwargs[isource], Iterable):  # pragma: no cover
                        raise Exception(f"Sampleable input {isource} must provide an iterable default value.")
                    self.input_space[isource] = kwargs[isource]
                elif isource in kwargs:
                    self.input_values[isource] = kwargs[isource]
                self.input[isource] = itarget
        self.output = outstr.split(",")
        self.id = _id
        self.metadata = _metadata
