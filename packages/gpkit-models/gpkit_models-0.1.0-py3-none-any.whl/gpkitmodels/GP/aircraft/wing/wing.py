"wing.py"

from builtins import range
from os import sep
from os.path import abspath, dirname

import numpy as np
import pandas as pd
from gpkit import Model, parse_variables

from gpkitmodels.tools.fit_constraintset import XfoilFit

from .capspar import CapSpar
from .wing_core import WingCore
from .wing_skin import WingSkin

# pylint: disable=no-member, invalid-name, unused-argument, exec-used
# pylint: disable=undefined-variable, attribute-defined-outside-init
# pylint: disable=too-many-instance-attributes


class Planform(Model):
    """Planform Area Definition

    Scalar Variables
    ---------
    S                                   [ft^2]  surface area
    AR                                  [-]     aspect ratio
    b                                   [ft]    span
    tau                                 [-]     airfoil thickness ratio
    CLmax           1.39                [-]     maximum lift coefficient
    CM              0.14                [-]     wing moment coefficient
    croot                               [ft]    root chord
    cmac                                [ft]    mean aerodynamic chord
    lam             0.5                 [-]     taper ratio
    cbarmac         self.return_cmac    [-]     non-dim MAC

    Variables of length N
    ---------------------
    eta         np.linspace(0,1,N)      [-]     (2y/b)
    cbar        self.return_c           [-]     non-dim chord at nodes

    Variables of length N-1
    -----------------------
    cave                                [ft]    mid section chord
    cbave       self.return_avg         [-]     non-dim mid section chord
    deta        self.return_deta        [-]     \\Delta (2y/b)

    Upper Unbounded
    ---------------  # bounding any pair of variables will work
    cave, b, tau

    Lower Unbounded
    ---------------
    cave, b, tau

    LaTex Strings
    -------------
    tau         \\tau
    CLmax       C_{L_{\\mathrm{max}}}
    CM          C_M
    croot       c_{\\mathrm{root}}
    cmac        c_{\\mathrm{MAC}}
    lam         \\lambda
    cbarmac     \\bar{c}_{\\mathrm{MAC}}

    """

    def return_c(self, c):
        "return normalized chord distribution"
        lam = c(self.lam).to("dimensionless").magnitude
        eta = c(self.eta).to("dimensionless").magnitude
        return np.array([2.0 / (1 + lam) * (1 + (lam - 1) * e) for e in eta])

    def return_cmac(self, c):
        "return normalized MAC"
        cbar = self.return_c(c)
        lam = cbar[1:] / cbar[:-1]
        maci = 2.0 / 3 * cbar[:-1] * (1 + lam + lam**2) / (1 + lam)
        deta = np.diff(c(self.eta))
        num = sum(
            [(cbar[i] + cbar[i + 1]) / 2 * maci[i] * deta[i] for i in range(len(deta))]
        )
        den = sum([(cbar[i] + cbar[i + 1]) / 2 * deta[i] for i in range(len(deta))])
        return num / den / cbar[0]

    return_avg = lambda self, c: (self.return_c(c)[:-1] + self.return_c(c)[1:]) / 2.0
    return_deta = lambda self, c: np.diff(c(self.eta))

    @parse_variables(__doc__, globals())
    def setup(self, N):
        return [
            b**2 == S * AR,
            cave == cbave * S / b,
            croot == S / b * cbar[0],
            cmac == croot * cbarmac,
        ]


class WingAero(Model):
    """Wing Aero Model

    Variables
    ---------
    Cd                      [-]     wing drag coefficient
    CL                      [-]     lift coefficient
    CLstall         1.3     [-]     stall CL
    e               0.9     [-]     span efficiency
    Re                      [-]     reynolds number
    cdp                     [-]     wing profile drag coefficient

    Upper Unbounded
    ---------------
    Cd, Re, static.planform.AR
    state.V, state.mu (if not muValue), state.rho (if not rhoValue)

    Lower Unbounded
    ---------------
    state.V, state.mu (if not muValue), state.rho (if not rhoValue)

    LaTex Strings
    -------------
    Cd              C_d
    CL              C_L
    CLstall         C_{L_{\\mathrm{stall}}}
    cdp             c_{d_p}

    """

    @parse_variables(__doc__, globals())
    def setup(
        self,
        static,
        state,
        fitdata=dirname(abspath(__file__)) + sep + "jho_fitdata.csv",
    ):
        self.state = state
        self.static = static

        df = pd.read_csv(fitdata)
        fd = df.to_dict(orient="records")[0]

        AR = static.planform.AR
        cmac = static.planform.cmac
        rho = state.rho
        V = state.V
        mu = state.mu
        # needed for Climb model in solar
        self.rhoValue = bool(rho.key.value)
        self.muValue = bool(mu.key.value)

        if fd["d"] == 2:
            independentvars = [CL, Re]
        elif fd["d"] == 3:
            independentvars = [CL, Re, static.planform.tau]

        return [
            Cd >= cdp + CL**2 / np.pi / AR / e,
            Re == rho * V * cmac / mu,
            # XfoilFit(fd, cdp, [CL, Re], airfoil="jho1.dat"),
            XfoilFit(fd, cdp, independentvars, name="polar"),
            CL <= CLstall,
        ]


class Wing(Model):
    """
    Wing Model

    Variables
    ---------
    W                   [lbf]       wing weight
    mfac        1.2     [-]         wing weight margin factor

    SKIP VERIFICATION

    Upper Unbounded
    ---------------
    W, planform.tau (if not sparJ)

    Lower Unbounded
    ---------------
    planform.b, spar.Sy (if sparModel), spar.J (if sparJ)

    LaTex Strings
    -------------
    mfac                m_{\\mathrm{fac}}

    """

    sparModel = CapSpar
    fillModel = WingCore
    flight_model = WingAero
    skinModel = WingSkin
    sparJ = False

    @parse_variables(__doc__, globals())
    def setup(self, N=5):
        self.N = N
        self.planform = Planform(N)
        self.components = []

        if self.skinModel:
            self.skin = self.skinModel(self.planform)
            self.components.extend([self.skin])
        if self.sparModel:
            self.spar = self.sparModel(N, self.planform)
            self.components.extend([self.spar])
            self.sparJ = hasattr(self.spar, "J")
        if self.fillModel:
            self.foam = self.fillModel(self.planform)
            self.components.extend([self.foam])

        constraints = [W / mfac >= sum(c["W"] for c in self.components)]

        return constraints, self.planform, self.components
