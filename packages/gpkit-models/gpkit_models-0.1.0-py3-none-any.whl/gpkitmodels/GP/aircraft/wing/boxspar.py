"box spar"

from gpkit import Model, SignomialsEnabled, parse_variables

from gpkitmodels import g
from gpkitmodels.GP.materials import cfrpfabric, cfrpud, foamhd

from .gustloading import GustL
from .sparloading import SparLoading

# pylint: disable=exec-used, undefined-variable, unused-argument, invalid-name


class BoxSpar(Model):
    """Box Spar Model

    Scalar Variables
    ----------------
    W                       [lbf]       spar weight
    wlim            0.15    [-]         spar width to chord ratio
    mfac            0.97    [-]         curvature knockdown factor
    tcoret          0.02    [-]         core to thickness ratio

    Variables of length N-1
    -----------------------
    hin                     [in]        height between caps
    I                       [m^4]       spar x moment of inertia
    Sy                      [m^3]       section modulus
    dm                      [kg]        segment spar mass
    w                       [in]        spar width
    d                       [in]        cross sectional diameter
    t                       [in]        spar cap thickness
    tshear                  [in]        shear web thickness
    tcore                   [in]        core thickness

    SKIP VERIFICATION

    Upper Unbounded
    ---------------
    W

    Lower Unbounded
    ---------------
    Sy, b, J, surface.deta

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
    tcoret                  (t_{\\mathrm{core}}/t)

    """

    loading = SparLoading
    gustloading = GustL
    material = cfrpud
    shearMaterial = cfrpfabric
    coreMaterial = foamhd

    @parse_variables(__doc__, globals())
    def setup(self, N, surface):
        self.surface = surface

        b = self.b = surface.b
        cave = self.cave = surface.cave
        tau = self.tau = surface.tau
        deta = surface.deta
        rho = self.material.rho
        rhoshear = self.shearMaterial.rho
        rhocore = self.coreMaterial.rho
        tshearmin = self.shearMaterial.tmin
        tmin = self.material.tmin

        self.weight = W >= 2 * dm.sum() * g

        constraints = [
            I / mfac <= w * t * hin**2,
            dm
            >= (
                rho * 4 * w * t
                + 4 * tshear * rhoshear * (hin + w)
                + 2 * rhocore * tcore * (w + hin)
            )
            * b
            / 2
            * deta,
            w <= wlim * cave,
            cave * tau >= hin + 4 * t + 2 * tcore,
            self.weight,
            t >= tmin,
            Sy * (hin / 2 + 2 * t + tcore) <= I,
            tshear >= tshearmin,
            tcore >= tcoret * cave * tau,
            d == w,
        ]

        return constraints
