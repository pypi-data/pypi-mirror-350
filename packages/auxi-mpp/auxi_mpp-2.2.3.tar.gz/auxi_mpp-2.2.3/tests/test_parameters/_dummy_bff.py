def dummy_bff(T: float, p: float, comps: dict[str, float]) -> dict[str, float]:
    cations = {"SiO2": "Si", "Al2O3": "Al", "CaO": "Ca", "MgO": "Mg"}

    test_bf: dict[str, float] = {
        f"{cations[k1]}-{cations[k2]}": v1 * v2 for k1, v1 in comps.items() for k2, v2 in comps.items()
    }

    return test_bf
