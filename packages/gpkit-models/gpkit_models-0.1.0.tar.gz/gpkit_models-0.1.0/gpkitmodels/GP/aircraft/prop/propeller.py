"propeller model"

import os

import pandas as pd
from gpkit import (
    Model,
    SignomialEquality,
    SignomialsEnabled,
    Variable,
    Vectorize,
    parse_variables,
)
from numpy import pi


class ActuatorProp(Model):
    """Propeller Model

    Variables
    ---------
    T                       [lbf]       thrust
    Tc                      [-]         coefficient of thrust
    etaadd     .7           [-]         swirl and nonuniformity losses
    etav       .85          [-]         viscous losses
    etai                    [-]         inviscid losses
    eta                     [-]         overall efficiency
    z1         self.helper  [-]         efficiency helper 1
    z2                      [-]         efficiency helper 2
    lam                     [-]         advance ratio
    CT                      [-]         thrust coefficient
    CP                      [-]         power coefficient
    Q                       [N*m]       torque
    omega                   [rpm]       propeller rotation rate
    omega_max  10000        [rpm]       max rotation rate
    P_shaft                 [kW]        shaft power
    M_tip      .5           [-]         Tip mach number
    a          295          [m/s]       Speed of sound at altitude
    """

    def helper(self, c):
        return 2.0 - 1.0 / c(self.etaadd)

    @parse_variables(__doc__, globals())
    def setup(self, static, state):
        V = state.V
        rho = state.rho
        R = static.R

        constraints = [
            eta <= etav * etai,
            Tc >= T / (0.5 * rho * V**2 * pi * R**2),
            z2 >= Tc + 1,
            etai * (z1 + z2**0.5 / etaadd) <= 2,
            lam >= V / (omega * R),
            CT >= Tc * lam**2,
            CP <= Q * omega / (0.5 * rho * (omega * R) ** 3 * pi * R**2),
            eta >= CT * lam / CP,
            omega <= omega_max,
            P_shaft == Q * omega,
            (M_tip * a) ** 2 >= (omega * R) ** 2 + V**2,
            static.T_m >= T,
        ]
        return constraints


class Propeller(Model):
    """Propeller Model

    Variables
    ---------
    R                               [ft]            prop radius
    W                               [lbf]           prop weight
    K           4e-4                [1/ft^2]        prop weight scaling factor
    T_m                             [lbf]           prop max static thrust

    Variables of length N
    ---------------------
    c                               [ft]            prop chord
    """

    flight_model = ActuatorProp

    @parse_variables(__doc__, globals())
    def setup(self, N=5):
        self.N = N
        return [W >= K * T_m * R**2]
