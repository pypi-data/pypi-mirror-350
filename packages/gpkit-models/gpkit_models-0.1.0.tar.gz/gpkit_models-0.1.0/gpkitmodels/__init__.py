"""GPkit Models - Library of exponential cone compatible sizing models"""

__version__ = "0.1.0"

from gpkit import Variable

g = Variable(
    "g", 9.81, "m/s^2", "earth surface gravitational acceleration", constant=True
)
