# gpkit-models

[![CI Status](https://github.com/beautifulmachines/gpkit-models/actions/workflows/tests.yml/badge.svg)](https://github.com/beautifulmachines/gpkit-models/actions/workflows/tests.yml)
[![CI Status](https://github.com/beautifulmachines/gpkit-models/actions/workflows/lint.yml/badge.svg)](https://github.com/beautifulmachines/gpkit-models/actions/workflows/lint.yml)

This repository contains those GP-/SP-compatible models that we consider well documented and general enough to be useful to multiple projects.

* **Simple models with in-depth explanations** (good for learning GPkit)
  * [SimPleAC](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/SP/SimPleAC/): a basic aircraft model that captures the fundamental design tradeoffs
  * [Economic Order Quantity](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/misc/Economic%20Order%20Quantity/): tradeoff between setup and holding costs
  * [Cylindrical Beam Moment of Inertia](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/misc/Moment%20of%20Inertia%20(cylindrical%20beam)): GP approximation of cylindrical beam MOI
  * [Net Present Value](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/misc/Net%20Present%20Value): financial tradeoff between cash and equipment
  * [Raymer Weights](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/misc/Raymer%20Weights): rule-of-thumb weight relations for aircraft design
* **GP models**
  * Aircraft
    * [Wing Structural and Aero Models](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/GP/aircraft/wing)
    * [Empennage](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/GP/aircraft/tail): TailBoom, HorizontalTail, and VerticalTail inherit from the Wing model
    * [Mission](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/GP/aircraft/mission): models that unify subsystems and flight profiles
    * [Fuselage](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/GP/aircraft/fuselage): elliptical and cylindrical fuselage models
    * [IC Gas Engine Model](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/GP/aircraft/engine)
  * [Bending Beam](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/GP/beam): discretized beam for distributed loads
* **SP models**
  * Aircraft
    * [Tail Boom Flexibility](https://github.com/beautifulmachines/gpkit-models/tree/main/gpkitmodels/SP/aircraft/tail/tail_boom_flex.py)
    * [Wing Spanwise Effectiveness](https://github.com/beautifulmachines/gpkit-models/blob/main/gpkitmodels/SP/aircraft/wing/wing.py)
  * Atmosphere
    * [Tony Tao's fits as (efficient) signomial equalities](https://github.com/beautifulmachines/gpkit-models/blob/main/gpkitmodels/SP/atmosphere/atmosphere.py). Valid until 10,000m of altitude. 

