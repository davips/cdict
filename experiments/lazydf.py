import numpy as np
from numpy import array
from pandas import DataFrame, Series

a = array([1, 2, 3])
b = array([5, 6, 7])
sa = Series(a, index=["um","dois","tres"])
sb = Series(b, index=["um","dois","tres"])
print(sa)
df = DataFrame({"a": sa, "b": sb}, copy=False)
a[1]=99
newsa = df["a"]
df["a"][1] = 66
print(newsa)
# print(df.index.to_series())
#
# print(df.shape, "================================")
# ar = df["a"].array[0]
# print(ar)
# a = np.reshape(ar, newshape=(len(df.iat[0, 0]),))
# a[0] = 11
# print(df)
# print()
#
# def column2np(df, colname):
#     import numpy as np
#     ar = df[colname].array[0]
#     return np.reshape(ar, newshape=(len(df.iat[0, 0]),))
#
# print(column2np(df,"b"))
# print()
# print(list(df.index))
