"tail aerodynamics"

import os

import pandas as pd
from gpkit import Model, parse_variables

from gpkitmodels.tools.fit_constraintset import FitCS

# pylint: disable=exec-used, attribute-defined-outside-init, undefined-variable
# pylint: disable=no-member


class TailAero(Model):
    """Tail Aero Model

    Variables
    ---------
    Re          [-]     Reynolds number
    Cd          [-]     drag coefficient

    Upper Unbounded
    ---------------
    Cd, Re, S, V, b, rho

    Lower Unbounded
    ---------------
    S, tau, V, b, rho

    LaTex Strings
    -------------
    Cd      C_d

    """

    @parse_variables(__doc__, globals())
    def setup(self, static, state):
        self.state = state

        cmac = self.cmac = static.planform.cmac
        b = self.b = static.planform.b
        S = self.S = static.planform.S
        tau = self.tau = static.planform.tau
        rho = self.rho = state.rho
        V = self.V = state.V
        mu = self.mu = state.mu
        path = os.path.dirname(__file__)
        fd = pd.read_csv(path + os.sep + "tail_dragfit.csv").to_dict(orient="records")[
            0
        ]

        constraints = [
            Re == V * rho * S / b / mu,
            # XfoilFit(fd, Cd, [Re, static["\\tau"]],
            #          err_margin="RMS", airfoil="naca 0008")
            FitCS(fd, Cd, [Re, tau], err_margin="RMS"),
        ]

        return constraints
