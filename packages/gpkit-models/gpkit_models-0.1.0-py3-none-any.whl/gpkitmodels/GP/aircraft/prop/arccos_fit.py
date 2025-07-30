from __future__ import print_function

import unittest

from gpfit.fit import fit
from numpy import arange, arccos, exp, log, log10, vstack
from numpy.random import random_sample

i = arange(0.0001, 3, 0.001)
j = arccos(exp(-i))
x = log(i)
y = log(j)
K = 1

cstrt, rmsErr = fit(x, y, K, "SMA")
print(rmsErr)
