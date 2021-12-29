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


class Let:
    def __init__(self, f: callable, in_out: str, /, **kwargs):
        if ":" not in in_out:
            raise Exception(f"Missing ':' in in_out schema ({in_out}).")
        in_, out = in_out.split(":")
        if out == "":
            raise Exception(f"Missing output field names after ':' in in_out schema ({in_out}).")
        self.f = f
        if in_ == "":
            self.input = [par.name for par in signature(f).parameters.values()]
        self.output = out.split(",")
