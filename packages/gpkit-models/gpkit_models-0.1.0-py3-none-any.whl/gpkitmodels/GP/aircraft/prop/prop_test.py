"propeller tests"

from gpkit import Model, units

from gpkitmodels.GP.aircraft.prop.propeller import ActuatorProp, Propeller
from gpkitmodels.GP.aircraft.wing.wing_test import FlightState
from gpkitmodels.SP.aircraft.prop.propeller import BladeElementProp


def simpleprop_test():
    "test simple propeller model"
    fs = FlightState()
    Propeller.flight_model = ActuatorProp
    p = Propeller()
    pp = p.flight_model(p, fs)
    m = Model(
        1 / pp.eta + p.W / (100.0 * units("lbf")) + pp.Q / (100.0 * units("N*m")),
        [fs, p, pp],
    )
    m.substitutions.update({"rho": 1.225, "V": 50, "T": 100, "omega": 1000})
    m.solve()


def ME_eta_test():

    fs = FlightState()
    Propeller.flight_model = BladeElementProp
    p = Propeller()
    pp = p.flight_model(p, fs)
    pp.substitutions[pp.T] = 100
    pp.cost = (
        1.0 / pp.eta + pp.Q / (1000.0 * units("N*m")) + p.T_m / (1000 * units("N"))
    )
    sol = pp.localsolve(iteration_limit=400)


def test():
    "tests"
    simpleprop_test()
    ME_eta_test()


if __name__ == "__main__":
    test()
