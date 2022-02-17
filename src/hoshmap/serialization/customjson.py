#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the idict project.
#  Please respect the license - more about this in the section (*) below.
#
#  idict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  idict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with idict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
from json import JSONEncoder

from hoshmap.value.ival import iVal
from hoshmap.value.strictival import StrictiVal


class CustomJSONEncoder(JSONEncoder):
    """
    >>> from hoshmap import idict
    >>> a = idict(x=3)
    >>> idict(d=a, y=5).show(colored=False)
    {
        d: {
            x: 3,
            _id: "fBb9FHVYpHC7vyM-B8UrXuN4oCcQ4Y7pnQ6oSK3J",
            _ids: {
                x: "KGWjj0iyLAn1RG6RTGtsGE3omZraJM6xO.kvG5pr"
            }
        },
        y: 5,
        _id: "YyAtuyiPhC7pHV-ADAoh1Lp30TM-08swr40vOmk1",
        _ids: {
            d: "fBb9FHVYpHC7vyM-B8UrXuN4oCcQ4Y7pnQ6oSK3J",
            y: "ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2"
        }
    }
    >>> from pandas.core.frame import DataFrame, Series
    >>> df = DataFrame([[1,2],[3,4]])
    >>> df
       0  1
    0  1  2
    1  3  4
    >>> b = idict(d=a, y=5, df=df, ell=...)
    >>> b.show(colored=False)
    {
        d: {
            x: 3,
            _id: "fBb9FHVYpHC7vyM-B8UrXuN4oCcQ4Y7pnQ6oSK3J",
            _ids: {
                x: "KGWjj0iyLAn1RG6RTGtsGE3omZraJM6xO.kvG5pr"
            }
        },
        y: 5,
        df: "«{0: {0: 1, 1: 3}, 1: {0: 2, 1: 4}}»",
        df_: {
            index: "«{0: 0, 1: 1}»",
            0: "«{0: 1, 1: 3}»",
            1: "«{0: 2, 1: 4}»",
            _id: "-sMsdSKphlBlTCE4unv9NJF35IPIPEboPoBmxwDa",
            _ids: {
                index: "DQa5yWRkGo-9FLqmaST8pbElYdUEgqF8xPvip6-3",
                0: "8ianf2LAQlxK7ZFvdOX.avsuK4L9FjUiMC7sM2Lm",
                1: "IIffH-qkWUFB.-VFd0z6BBrIpfvNuc8GPxlQYgg3"
            }
        },
        ell: "...",
        _id: "ylziFtJ74K-m39S3rhlZfJ1yEADwIxsTaUi4g2D.",
        _ids: {
            d: "fBb9FHVYpHC7vyM-B8UrXuN4oCcQ4Y7pnQ6oSK3J",
            y: "ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2",
            df: "-sMsdSKphlBlTCE4unv9NJF35IPIPEboPoBmxwDa",
            ell: "P1oPe-8hTjTdV6gKov4oIQnmTUXyD2fU6E7C8MS6"
        }
    }
    >>> from numpy import array
    >>> idict(b=b, z=9, c=(c:=array([1,2,3])), d=Series(c), dd=array([[1, 2], [3, 4]])).show(colored=False)
    {
        b: {
            d: {
                x: 3,
                _id: "fBb9FHVYpHC7vyM-B8UrXuN4oCcQ4Y7pnQ6oSK3J",
                _ids: {
                    x: "KGWjj0iyLAn1RG6RTGtsGE3omZraJM6xO.kvG5pr"
                }
            },
            y: 5,
            df: "«{0: {0: 1, 1: 3}, 1: {0: 2, 1: 4}}»",
            df_: {
                index: "«{0: 0, 1: 1}»",
                0: "«{0: 1, 1: 3}»",
                1: "«{0: 2, 1: 4}»",
                _id: "-sMsdSKphlBlTCE4unv9NJF35IPIPEboPoBmxwDa",
                _ids: {
                    index: "DQa5yWRkGo-9FLqmaST8pbElYdUEgqF8xPvip6-3",
                    0: "8ianf2LAQlxK7ZFvdOX.avsuK4L9FjUiMC7sM2Lm",
                    1: "IIffH-qkWUFB.-VFd0z6BBrIpfvNuc8GPxlQYgg3"
                }
            },
            ell: "...",
            _id: "ylziFtJ74K-m39S3rhlZfJ1yEADwIxsTaUi4g2D.",
            _ids: {
                d: "fBb9FHVYpHC7vyM-B8UrXuN4oCcQ4Y7pnQ6oSK3J",
                y: "ecvgo-CBPi7wRWIxNzuo1HgHQCbdvR058xi6zmr2",
                df: "-sMsdSKphlBlTCE4unv9NJF35IPIPEboPoBmxwDa",
                ell: "P1oPe-8hTjTdV6gKov4oIQnmTUXyD2fU6E7C8MS6"
            }
        },
        z: 9,
        c: "«[1 2 3]»",
        d: "«{0: 1, 1: 2, 2: 3}»",
        dd: "«[[1 2] [3 4]]»",
        _id: "pklpcC04mjnBVPnUHYQX2Xp64gBYV1lpCz6hTThl",
        _ids: {
            b: "ylziFtJ74K-m39S3rhlZfJ1yEADwIxsTaUi4g2D.",
            z: "GuwIQCrendfKXZr5jGfrUwoP-8TWMhmLHYrja2yj",
            c: "QkfVsy7ITAmoIiOFgbYpsQodBSIYshhiUm3v2r8d",
            d: "5iU-DAFL3XTLno88g056s2G12RidCKkCgLCLIwB5",
            dd: "fVj30baMeet4PcN9ZY-8uMpFin89FY8h8MI4RkDd"
        }
    }
    """

    width = 200

    def default(self, obj):
        if obj is not None:
            if obj is Ellipsis:
                return "..."
            if isinstance(obj, iVal) and obj.isevaluated:
                return obj.value
            # if isinstance(obj, FunctionType):
            #     return str(obj)
            if not isinstance(obj, (list, set, str, int, float, bytearray, bool)):
                if obj.__class__.__name__ in ["DataFrame", "Series"]:
                    # «str()» is to avoid nested identation
                    return f"«{truncate(str(obj.to_dict()), self.width)}»"
                if obj.__class__.__name__ == "ndarray":
                    txt = str(obj).replace('\n', '')
                    return f"«{truncate(txt, self.width)}»"
                return truncate(str(obj).replace("\n", ""), self.width)
        return JSONEncoder.default(self, obj)  # pragma: no cover


# class CustomJSONDecoder(JSONDecoder):
#     def __init__(self, *args, **kwargs):
#         JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
#
#     def object_hook(self, obj):
#         if obj is not None:
#             if isinstance(obj, str) and len(obj) == digits:
#                 return
#         return obj


def truncate(txt, width=200):
    if len(txt) > width:
        txt = txt[:width] + (" ...»" if txt.endswith("»") else " ...")
    return txt
