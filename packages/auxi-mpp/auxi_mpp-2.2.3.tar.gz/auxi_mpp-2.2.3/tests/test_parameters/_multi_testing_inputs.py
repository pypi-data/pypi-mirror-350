from ..test_parameters._dummy_bff import dummy_bff


multi_testing_inputs = [
    # temperature limits
    (1000, {"SiO2": 0.4, "Al2O3": 0.4, "CaO": 0.2}, dummy_bff),
    (2500, {"SiO2": 0.25, "Al2O3": 0.25, "CaO": 0.25, "MgO": 0.25}, dummy_bff),
    # pure substance conditions
    (1500, {"SiO2": 1.0, "Al2O3": 0.0, "CaO": 0.0, "MgO": 0.0}, dummy_bff),
    (1500, {"SiO2": 0.01, "Al2O3": 0.99, "CaO": 0.0, "MgO": 0.0}, dummy_bff),
    (1500, {"SiO2": 0.01, "Al2O3": 0.0, "CaO": 0.99, "MgO": 0.0}, dummy_bff),
    (1500, {"SiO2": 0.01, "Al2O3": 0.0, "CaO": 0.0, "MgO": 0.99}, dummy_bff),
]

multi_error_test_inputs = [
    # contain SiO2?
    (1500, {"SiO2": 0.0, "Al2O3": 0.4, "CaO": 0.4, "MgO": 0.2}, dummy_bff),
    (1500, {"CaO": 0.4, "Al2O3": 0.4, "MgO": 0.2}, dummy_bff),
    # inside T boundaries?
    (2501, {"SiO2": 0.4, "CaO": 0.4, "MgO": 0.2}, dummy_bff),
    (999, {"SiO2": 0.4, "MgO": 0.4, "Al2O3": 0.2}, dummy_bff),
    # inside x boundaries?
    (1500, {"SiO2": -0.1, "Al2O3": 0.4, "CaO": 0.4, "MgO": 0.3}, dummy_bff),
    (1500, {"SiO2": 1.1, "Al2O3": -0.04, "CaO": -0.04, "MgO": -0.02}, dummy_bff),
    (1500, {"MgO": -0.1, "SiO2": 0.4, "Al2O3": 0.4, "CaO": 0.3}, dummy_bff),
    (1500, {"MgO": 1.1, "SiO2": -0.04, "Al2O3": -0.04, "CaO": -0.02}, dummy_bff),
    (1500, {"CaO": -0.1, "MgO": 0.4, "SiO2": 0.4, "Al2O3": 0.3}, dummy_bff),
    (1500, {"CaO": 1.1, "MgO": -0.04, "SiO2": -0.04, "Al2O3": -0.02}, dummy_bff),
    (1500, {"Al2O3": -0.1, "CaO": 0.4, "MgO": 0.4, "SiO2": 0.3}, dummy_bff),
    (1500, {"Al2O3": 1.1, "CaO": -0.04, "MgO": -0.04, "SiO2": -0.02}, dummy_bff),
    # add up to 1?
    (1500, {"SiO2": 0.25, "Al2O3": 0.25, "CaO": 0.25, "MgO": 0.2}, dummy_bff),
    (1500, {"SiO2": 0.25, "Al2O3": 0.25, "CaO": 0.25, "MgO": 0.3}, dummy_bff),
    # too few compounds are provided
    (1500, {"SiO2": 0.6, "Al2O3": 0.4}, dummy_bff),
    (1500, {"SiO2": 1.0}, dummy_bff),
    # invalid compound provided
    (1500, {"SiO2": 0.4, "FeO": 0.4, "Al2O3": 0.2}, dummy_bff),
]

binary_vs_multi_test_inputs = [
    # temperature limits
    (1000, {"SiO2": 0.5, "Al2O3": 0.5}),
    (2500, {"SiO2": 0.5, "CaO": 0.5}),
    # pure substance conditions
    (1500, {"SiO2": 1.0, "MgO": 0.0}),
    (1500, {"SiO2": 0.01, "Al2O3": 0.99}),
    (1500, {"SiO2": 0.01, "CaO": 0.99}),
    (1500, {"SiO2": 0.01, "MgO": 0.99}),
]

multi3_vs_multi4_test_inputs = [
    # temperature limits
    (1000, {"SiO2": 0.4, "Al2O3": 0.4, "CaO": 0.2}),
    (2500, {"SiO2": 0.4, "Al2O3": 0.4, "MgO": 0.2}),
    # trace amount of SiO2
    (1500, {"SiO2": 1.0, "CaO": 0.0, "MgO": 0.0}),
    (1500, {"SiO2": 0.01, "Al2O3": 0.99, "CaO": 0.0}),
    (1500, {"SiO2": 0.01, "CaO": 0.99, "MgO": 0.0}),
    (1500, {"SiO2": 0.01, "MgO": 0.99, "Al2O3": 0.0}),
]

pre_optimisation_params = [
    # pure substance conditions - unary and binaries
    {"AlO15": 0.0, "CaO": 0.0, "MgO": 0.0},
    {"AlO15": 0.99, "CaO": 0.0, "MgO": 0.0},
    {"AlO15": 0.0, "CaO": 0.99, "MgO": 0.0},
    {"AlO15": 0.0, "CaO": 0.0, "MgO": 0.99},
    # ternary systems
    {"AlO15": 0.2, "CaO": 0.2, "MgO": 0.0},
    {"AlO15": 0.2, "CaO": 0.0, "MgO": 0.2},
    {"AlO15": 0.0, "CaO": 0.2, "MgO": 0.2},
    # quaternary system
    {"AlO15": 0.2, "CaO": 0.2, "MgO": 0.2},
]
