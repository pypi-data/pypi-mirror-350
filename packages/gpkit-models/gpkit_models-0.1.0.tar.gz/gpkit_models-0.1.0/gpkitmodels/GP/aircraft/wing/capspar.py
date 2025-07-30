"cap spar"

from gpkit import Model, parse_variables

from gpkitmodels import g
from gpkitmodels.GP.materials import cfrpfabric, cfrpud, foamhd

from .gustloading import GustL
from .sparloading import SparLoading

# pylint: disable=exec-used, undefined-variable, unused-argument, invalid-name


class CapSpar(Model):
    """Cap Spar Model

    Scalar Variables
    ----------------
    E               2e7     [psi]       Young modulus of CFRP
    W                       [lbf]       spar weight
    wlim            0.15    [-]         spar width to chord ratio
    mfac            0.97    [-]         curvature knockdown factor

    Variables of length N-1
    -----------------------
    hin                     [in]        height between caps
    I                       [m^4]       spar x moment of inertia
    Sy                      [m^3]       section modulus
    dm                      [kg]        segment spar mass
    w                       [in]        spar width
    t                       [in]        spar cap thickness
    tshear                  [in]        shear web thickness

    Upper Unbounded
    ---------------
    W, cave, tau

    Lower Unbounded
    ---------------
    Sy, b, surface.deta

    LaTex Strings
    -------------
    wlim                    w_{\\mathrm{lim}}
    mfac                    m_{\\mathrm{fac}}
    hin                     h_{\\mathrm{in}_i}
    I                       I_i
    Sy                      S_{y_i}
    dm                      \\Delta{m}
    w                       w_i
    t                       t_i
    tshear                  t_{\\mathrm{shear}_i}

    """

    loading = SparLoading
    gustloading = GustL
    material = cfrpud
    shearMaterial = cfrpfabric
    coreMaterial = foamhd

    @parse_variables(__doc__, globals())
    def setup(self, N, surface):
        self.surface = surface

        cave = self.cave = surface.cave
        b = self.b = surface.b
        deta = surface.deta
        tau = self.tau = surface.tau
        rho = self.material.rho
        rhoshear = self.shearMaterial.rho
        rhocore = self.coreMaterial.rho
        tshearmin = self.shearMaterial.tmin

        return [
            I / mfac <= 2 * w * t * (hin / 2) ** 2,
            dm
            >= (
                rho * (2 * w * t)
                + 2 * tshear * rhoshear * (hin + 2 * t)
                + rhocore * w * hin
            )
            * b
            / 2
            * deta,
            W >= 2 * dm.sum() * g,
            w <= wlim * cave,
            cave * tau >= hin + 2 * t,
            Sy * (hin / 2 + t) <= I,
            tshear >= tshearmin,
        ]
