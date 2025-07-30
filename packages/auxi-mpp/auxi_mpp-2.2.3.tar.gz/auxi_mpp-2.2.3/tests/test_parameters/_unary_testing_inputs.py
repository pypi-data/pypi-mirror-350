unary_testing_inputs = [
    # temperature limits
    (1000, {"SiO2": 1.0}),
    (1000, {"Al2O3": 1.0}),
    (1000, {"CaO": 1.0}),
    (1000, {"MgO": 1.0}),
    (2500, {"SiO2": 1.0}),
    (2500, {"Al2O3": 1.0}),
    (2500, {"CaO": 1.0}),
    (2500, {"MgO": 1.0}),
]

unary_error_test_inputs = [
    # inside T boundaries?
    (2501, {"SiO2": 1.0}),
    (999, {"Al2O3": 1.0}),
    # inside x boundaries?
    (1500, {"CaO": 0.9}),
    (1500, {"MgO": 1.1}),
    # invalid compound provided
    (1500, {"FeO": 1.0}),
    # too many compounds provided
    (1500, {"SiO2": 0.5, "MgO": 0.5}),
]
