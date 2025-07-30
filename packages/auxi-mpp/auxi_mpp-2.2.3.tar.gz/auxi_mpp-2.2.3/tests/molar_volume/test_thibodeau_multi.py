"""Test ThibodeauMulti model."""

from collections.abc import Callable

import pytest

from auxi.mpp.slag.Vm._thibodeau_binary import ThibodeauBinary
from auxi.mpp.slag.Vm._thibodeau_multi import ThibodeauMulti

from ..test_parameters._dummy_bff import dummy_bff
from ..test_parameters._multi_testing_inputs import (
    binary_vs_multi_test_inputs,
    multi3_vs_multi4_test_inputs,
    multi_error_test_inputs,
    multi_testing_inputs,
)


# tests that should pass
@pytest.mark.parametrize("temperature, composition, bff", multi_testing_inputs)
def test_thibodeau_multi(
    temperature: float, composition: dict[str, float], bff: Callable[[float, float, dict[str, float]], dict[str, float]]
):
    """Test temperature and composition limits."""
    model = ThibodeauMulti(bff=bff)
    result = model.calculate(T=temperature, x=composition)

    assert result > 0


# tests that should fail
@pytest.mark.parametrize("temperature, composition, bff", multi_error_test_inputs)
def test_thibodeau_multi_errors(
    temperature: float, composition: dict[str, float], bff: Callable[[float, float, dict[str, float]], dict[str, float]]
):
    """Test if invalid inputs will fail."""
    model = ThibodeauMulti(bff=bff)
    with pytest.raises(ValueError):
        model.calculate(T=temperature, x=composition)


# test against the binary model
@pytest.mark.parametrize("temperature, composition", binary_vs_multi_test_inputs)
def test_mv_binary_vs_multi(temperature: float, composition: dict[str, float]):
    """Test if the binary and multi model agrees."""
    binary_model = ThibodeauBinary(bff=dummy_bff)
    multi_model = ThibodeauMulti(bff=dummy_bff)

    four_comps = {"SiO2": 0.0, "Al2O3": 0.0, "CaO": 0.0, "MgO": 0.0}
    for comp, value in composition.items():
        if comp in four_comps:
            four_comps[comp] = value

    binary_result = binary_model.calculate(T=temperature, x=composition)
    multi_result = multi_model.calculate(T=temperature, x=four_comps)

    assert abs(multi_result - binary_result) <= 1e-9


# test three and four component input for the same three component system
@pytest.mark.parametrize("temperature, composition", multi3_vs_multi4_test_inputs)
def test_mv_multi3_vs_multi4(temperature: float, composition: dict[str, float]):
    """Test if the multi model agrees when three and four components is specified."""
    multi3_model = ThibodeauMulti(bff=dummy_bff)
    multi4_model = ThibodeauMulti(bff=dummy_bff)

    four_comps = {"SiO2": 0.0, "Al2O3": 0.0, "CaO": 0.0, "MgO": 0.0}
    for comp, value in composition.items():
        if comp in four_comps:
            four_comps[comp] = value

    multi3_result = multi3_model.calculate(T=temperature, x=composition)
    multi4_result = multi4_model.calculate(T=temperature, x=four_comps)

    assert abs(multi4_result - multi3_result) <= 1e-9


def test_loaded_parameters():
    """Test if parameters loads normally."""
    model = ThibodeauMulti(bff=dummy_bff)

    assert model.property == "Molar Volume"
    assert model.symbol == "Vm"
    assert model.display_symbol == "\\bar{V}"
    assert model.units == "\\cubic\\meter\\per\\mol"
    assert model.material == "Slag"
    assert model.references == ["thibodeau2016-part2", "thibodeau2016-part3"]

    assert model.bff == dummy_bff
    assert model.n_O["SiO2"] == 2
    assert model.cation["Al2O3"] == "Al"
    assert model.Q["CaO"][0]["a"] == 50.7
    assert model.Q["MgO"][4]["b"] == 0.7e-3
    assert model.cation_count["Al2O3"] == 2
    assert sorted(model.compound_scope) == ["Al2O3", "CaO", "MgO", "SiO2"]


def test_abstract_calc():
    """Test if calling the calculate() method implicitly works correctly."""
    model = ThibodeauMulti(bff=dummy_bff)
    result1 = model.calculate(T=1700, x={"SiO2": 0.25, "Al2O3": 0.25, "CaO": 0.25, "MgO": 0.25})
    result2 = model(T=1700, x={"SiO2": 0.25, "Al2O3": 0.25, "CaO": 0.25, "MgO": 0.25})

    assert abs(result1 - result2) < 1e-9
