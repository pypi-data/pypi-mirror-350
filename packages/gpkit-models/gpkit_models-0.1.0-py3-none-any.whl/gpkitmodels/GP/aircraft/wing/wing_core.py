"wing interior"

from gpkit import Model, parse_variables

from gpkitmodels import g
from gpkitmodels.GP.materials import foamhd

# pylint: disable=exec-used, no-member, undefined-variable


class WingCore(Model):
    """Wing Core Model

    Variables
    ---------
    W                           [lbf]       wing core weight
    Abar            0.0753449   [-]         normalized cross section area

    Upper Unbounded
    ---------------
    W

    Lower Unbounded
    ---------------
    cave, b, surface.deta

    LaTex Strings
    -------------
    rhocore                 \\rho_{\\mathrm{core}}
    Abar                    \\bar{A}

    """

    material = foamhd

    @parse_variables(__doc__, globals())
    def setup(self, surface):
        self.surface = surface

        cave = self.cave = surface.cave
        b = self.b = surface.b
        deta = surface.deta
        rho = self.material.rho

        return [W >= 2 * (g * rho * Abar * cave**2 * b / 2 * deta).sum()]
