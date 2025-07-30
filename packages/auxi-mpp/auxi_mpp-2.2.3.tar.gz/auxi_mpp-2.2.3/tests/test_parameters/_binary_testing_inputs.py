from ..test_parameters._dummy_bff import dummy_bff


binary_testing_inputs = [
    # temperature limits
    (1000, {"SiO2": 0.5, "Al2O3": 0.5}, dummy_bff),
    (2500, {"SiO2": 0.5, "Al2O3": 0.5}, dummy_bff),
    # pure substance conditions
    (1500, {"SiO2": 1.0, "Al2O3": 0.0}, dummy_bff),
    (1500, {"SiO2": 1.0, "CaO": 0.0}, dummy_bff),
    (1500, {"SiO2": 1.0, "MgO": 0.0}, dummy_bff),
    (1500, {"SiO2": 0.01, "Al2O3": 0.99}, dummy_bff),
    (1500, {"SiO2": 0.01, "CaO": 0.99}, dummy_bff),
    (1500, {"SiO2": 0.01, "MgO": 0.99}, dummy_bff),
]

binary_error_test_inputs = [
    # contain SiO2?
    (1500, {"SiO2": 0.0, "Al2O3": 1.0}, dummy_bff),
    (1500, {"SiO2": 0.0, "CaO": 1.0}, dummy_bff),
    (1500, {"SiO2": 0.0, "MgO": 1.0}, dummy_bff),
    (1500, {"CaO": 0.5, "Al2O3": 0.5}, dummy_bff),
    (1500, {"MgO": 0.5, "CaO": 0.5}, dummy_bff),
    (1500, {"Al2O3": 0.5, "MgO": 0.5}, dummy_bff),
    # inside T boundaries?
    (2501, {"SiO2": 0.5, "Al2O3": 0.5}, dummy_bff),
    (999, {"SiO2": 0.5, "CaO": 0.5}, dummy_bff),
    # inside x boundaries?
    (1500, {"SiO2": -0.1, "Al2O3": 1.1}, dummy_bff),
    (1500, {"SiO2": -0.1, "CaO": 1.1}, dummy_bff),
    (1500, {"SiO2": -0.1, "MgO": 1.1}, dummy_bff),
    (1500, {"SiO2": 1.1, "Al2O3": -0.1}, dummy_bff),
    (1500, {"SiO2": 1.1, "CaO": -0.1}, dummy_bff),
    (1500, {"SiO2": 1.1, "MgO": -0.1}, dummy_bff),
    # add up to 1?
    (1500, {"SiO2": 0.4, "CaO": 0.4}, dummy_bff),
    (1500, {"SiO2": 0.6, "MgO": 0.6}, dummy_bff),
    # too many and too few components provided
    (1500, {"SiO2": 1.0}, dummy_bff),
    (1500, {"SiO2": 0.4, "CaO": 0.4, "Al2O3": 0.2}, dummy_bff),
    # invalid compound provided
    (1500, {"SiO2": 0.5, "FeO": 0.5}, dummy_bff),
]
