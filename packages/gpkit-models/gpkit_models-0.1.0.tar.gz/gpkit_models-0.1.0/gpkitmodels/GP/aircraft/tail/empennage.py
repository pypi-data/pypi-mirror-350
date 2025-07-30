"empennage.py"

from gpkit import Model, parse_variables

from .horizontal_tail import HorizontalTail
from .tail_boom import TailBoom, TailBoomState
from .vertical_tail import VerticalTail


# pylint: disable=attribute-defined-outside-init, no-member, exec-used
# pylint: disable=too-many-instance-attributes, invalid-name, undefined-variable
class Empennage(Model):
    """empennage model, consisting of vertical, horizontal and tailboom

    Variables
    ---------
    mfac        1.0     [-]     tail weight margin factor
    W                   [lbf]   empennage weight

    SKIP VERIFICATION

    Upper Unbounded
    ---------------
    W, vtail.Vv, htail.Vh, tailboom.cave (if not tbSecWeight)
    htail.planform.tau (if not hSparModel)
    vtail.planform.tau (if not vSparModel)

    Lower Unbounded
    ---------------
    htail.lh, htail.Vh, htail.planform.b, htail.mh
    vtail.lv, vtail.Vv, vtail.planform.b
    htail.planform.tau (if not hSparModel)
    vtail.planform.tau (if not vSparModel)
    htail.spar.Sy (if hSparModel), htail.spar.J (if hSparModel)
    vtail.spar.Sy (if vSparModel), vtail.spar.J (if vSparModel)
    tailboom.Sy, tailboom.cave (if not tbSecWeight), tailboom.J (if tbSecWeight)

    LaTex Strings
    -------------
    mfac        m_{\\mathrm{fac}}

    """

    @parse_variables(__doc__, globals())
    def setup(self, N=2):
        self.htail = HorizontalTail()
        self.hSparModel = self.htail.sparModel
        self.htail.substitutions.update({self.htail.mfac: 1.1})
        lh = self.lh = self.htail.lh
        self.vtail = VerticalTail()
        self.vSparModel = self.vtail.sparModel
        self.vtail.substitutions.update({self.vtail.mfac: 1.1})
        lv = self.lv = self.vtail.lv
        self.tailboom = TailBoom(N=N)
        self.tbSecWeight = self.tailboom.secondaryWeight
        self.components = [self.htail, self.vtail, self.tailboom]
        l = self.l = self.tailboom.l

        constraints = [
            W / mfac >= sum(c.W for c in self.components),
            l >= lh,
            l >= lv,
        ]

        return self.components, constraints
