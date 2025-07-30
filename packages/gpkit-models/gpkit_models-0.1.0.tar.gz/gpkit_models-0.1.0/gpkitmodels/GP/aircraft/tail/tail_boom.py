"tail boom model"

from gpkit import Model, Variable, VectorVariable, parse_variables, units
from numpy import pi

from gpkitmodels import g
from gpkitmodels.GP.beam.beam import Beam

from .tube_spar import TubeSpar

# pylint: disable=exec-used, undefined-variable, invalid-name
# pylint: disable=attribute-defined-outside-init


class TailBoomAero(Model):
    """Tail Boom Aero Model

    Variables
    ---------
    Cf          [-]     tail boom skin friction coefficient
    Re          [-]     tail boom reynolds number

    Upper Unbounded
    ---------------
    Re, Cf, l, V, rho

    Lower Unbounded
    ---------------
    l, V, rho

    LaTex Strings
    -------------
    Cf      C_f

    """

    @parse_variables(__doc__, globals())
    def setup(self, static, state):
        self.state = state

        l = self.l = static.l
        rho = self.rho = state.rho
        V = self.V = state.V
        mu = self.mu = state.mu

        return [
            Re == V * rho * l / mu,
            Cf >= 0.455 / Re**0.3,
        ]


class TailBoomState(Model):
    """Tail Boom Loading State

    Variables
    ---------
    rhosl           1.225           [kg/m^3]    air density at sea level
    Vne             40              [m/s]       never exceed vehicle speed

    LaTex Strings
    -------------
    rhosl           \\rho_{\\mathrm{sl}}
    Vne             V_{\\mathrm{NE}}

    """

    @parse_variables(__doc__, globals())
    def setup(self):
        pass


class VerticalBoomTorsion(Model):
    """Tail Boom Torsion from Vertical Tail

    Variables
    ---------
    T                           [N*m]       vertical tail moment
    taucfrp         210         [MPa]       torsional stress limit of carbon

    Upper Unbounded
    ---------------
    J

    Lower Unbounded
    ---------------
    d0, b, S

    LaTex Strings
    -------------
    taucfrp     \\tau_{\\mathrm{CFRP}}

    """

    @parse_variables(__doc__, globals())
    def setup(self, tailboom, vtail, state):
        J = self.J = tailboom.J
        d0 = self.d0 = tailboom.d
        b = self.b = vtail.planform.b
        S = self.S = vtail.planform.S
        rhosl = self.rhosl = state.rhosl
        Vne = self.Vne = state.Vne
        CLmax = vtail.planform.CLmax

        return [T >= 0.5 * rhosl * Vne**2 * S * CLmax * b, taucfrp >= T * d0 / 2 / J]


class TailBoomBending(Model):
    """Tail Boom Bending

    Variables
    ---------
    F                       [N]     tail force
    th                      [-]     tail boom deflection angle
    kappa           0.1     [-]     max tail boom deflection
    Nsafety         1.0     [-]     safety load factor

    Variables of length tailboom.N-1
    --------------------------------
    Mr                      [N*m]   section root moment


    Upper Unbounded
    ---------------
    tailboom.I0, tailboom.Sy
    tailboom.J (if tailboomJ), tailboom.I

    Lower Unbounded
    ---------------
    htail.planform.S, htail.planform.CLmax
    tailboom.l, tailboom.deta
    state.qne

    LaTex Strings
    -------------
    th      \\theta
    thmax   \\theta_{\\mathrm{max}}

    """

    @parse_variables(__doc__, globals())
    def setup(self, tailboom, htail, state):
        N = self.N = tailboom.N
        self.state = state
        self.htail = htail
        self.tailboom = tailboom

        Beam.qbarFun = [1e-10] * N
        Beam.SbarFun = [1.0] * N
        beam = self.beam = Beam(N)

        I = tailboom.I
        tailboom.I0 = I[0]
        l = tailboom.l
        S = htail.planform.S
        E = tailboom.material.E
        Sy = tailboom.Sy
        qne = state.qne
        CLmax = htail.planform.CLmax
        deta = tailboom.deta
        sigma = tailboom.material.sigma

        constraints = [
            beam.dx == deta,
            F >= qne * S,
            beam["\\bar{EI}"] <= E * I / F / l**2 / 2,
            Mr >= beam["\\bar{M}"][:-1] * F * l,
            sigma >= Mr / Sy,
            th == beam["\\theta"][-1],
            beam["\\bar{\\delta}"][-1] * CLmax * Nsafety <= kappa,
        ]

        self.tailboomJ = hasattr(tailboom, "J")
        if self.tailboomJ:
            constraints.append(tailboom.J >= 1e-10 * units("m^4"))

        return constraints, beam


class TailBoom(TubeSpar):
    """Tail Boom Model

    Variables
    ---------
    l                           [ft]        tail boom length
    S                           [ft^2]      tail boom surface area
    b                           [ft]        twice tail boom length
    deta          1./(N-1)      [-]         normalized segment length
    tau           1.0           [-]         thickness to width ratio
    rhoA          0.15          [kg/m^2]    total aerial density

    Variables of length N-1
    -----------------------
    cave                        [in]        average segment width

    """

    flight_model = TailBoomAero
    tailLoad = TailBoomBending
    secondaryWeight = None

    @parse_variables(__doc__, globals())
    def setup(self, N=5):
        self.N = N
        self.spar = super(TailBoom, self).setup(N, self)

        if self.secondaryWeight:
            self.weight.right += rhoA * g * S

        d0 = self.d0 = self.d[0]

        return self.spar, [S == l * pi * d0, b == 2 * l]
