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
import pickle
from typing import Union

from cdict.value.ival import iVal
from hosh import Hosh


class StrictiVal(iVal):
    """
    Identified value

    >>> StrictiVal(2)
    2
    """

    def __init__(self, value, id: Union[str, Hosh] = None):
        self.value = value
        self.hosh = Hosh(pickle.dumps(value, protocol=5)) if id is None else self.handle_id(id)
        self.result = {self.hosh.id: value}

    def __repr__(self):
        return repr(self.value)
