"tube spar for wing"

from chord_spar_loading import ChordSparL
from gpkit import Model, Variable, Vectorize
from numpy import pi


class TubeSpar(Model):
    "tube spar model"

    def setup(self, b, cave, tau, N=5):
        self.N = N

        rho_cfrp = Variable("\\rho_{CFRP}", 1.6, "g/cm^3", "density of CFRP")
        E = Variable("E", 2e7, "psi", "Youngs modulus of CF")

        with Vectorize(self.N - 1):
            d = Variable("d", "in", "spar diameter")
            I = Variable("I", "m^4", "spar x moment of inertia")
            Sy = Variable("S_y", "m**3", "section modulous")
            A = Variable("A", "in**2", "spar cross sectional area")
            dm = Variable("dm", "kg", "segment spar mass")

        W = Variable("W", "lbf", "tube spar weight")
        g = Variable("g", 9.81, "m/s**2", "gravitational constant")

        constraints = [
            dm >= rho_cfrp * A * b / (N - 1),
            W >= 2 * dm.sum() * g,
            cave * tau >= d,
            4 * I**2 / A**2 / (d / 2) ** 2 + A / pi <= (d / 2) ** 2,
            Sy * (d / 2) <= I,
            E == E,
        ]

        return constraints

    def loading(self, Wcent):
        return ChordSparL(self, Wcent)
