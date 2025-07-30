"wing.py"

import numpy as np
from gpkit import SignomialsEnabled, parse_variables

from gpkitmodels.GP.aircraft.wing.wing import Wing as WingGP

# pylint: disable=attribute-defined-outside-init, invalid-name


class Wing(WingGP):
    """SP wing model

    Variables
    ---------
    mw          [-]     span wise effectiveness

    """

    @parse_variables(__doc__, globals())
    def setup(self, N=5):
        self.wing = WingGP.setup(self, N=N)
        with SignomialsEnabled():
            constraints = [mw * (1 + 2 / self.planform["AR"]) >= 2 * np.pi]

        return self.wing, constraints
