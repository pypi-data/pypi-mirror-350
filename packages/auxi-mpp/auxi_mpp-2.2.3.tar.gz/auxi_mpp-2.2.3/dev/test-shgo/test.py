"""Testing."""

from auxi.mpp.slag.D import ThibodeauIDBinary


def dummy_bff(T: float, p: float, comps: dict[str, float]) -> dict[str, float]:
    """Bond fraction function."""
    cations = {"SiO2": "Si", "Al2O3": "Al", "CaO": "Ca", "MgO": "Mg"}

    test_bf: dict[str, float] = {
        f"{cations[k1]}-{cations[k2]}": v1 * v2 for k1, v1 in comps.items() for k2, v2 in comps.items()
    }

    return test_bf


model_binary = ThibodeauIDBinary(bff=dummy_bff)
print(model_binary.compound_scope)
result = model_binary.calculate(T=1000, x={"SiO2": 0.5, "Al2O3": 0.5})
print(result)
