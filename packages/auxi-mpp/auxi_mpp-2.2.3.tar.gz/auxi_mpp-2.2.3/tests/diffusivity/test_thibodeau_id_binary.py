"""Test ThibodeauIDBinary model."""

from collections.abc import Callable

import pytest

from auxi.mpp.slag.D._thibodeau_id_binary import ThibodeauIDBinary

from ..test_parameters._binary_testing_inputs import binary_error_test_inputs, binary_testing_inputs
from ..test_parameters._dummy_bff import dummy_bff


# tests that should pass
@pytest.mark.parametrize("temperature, composition, bff", binary_testing_inputs)
def test_thibodeau_id_binary(
    temperature: float, composition: dict[str, float], bff: Callable[[float, float, dict[str, float]], dict[str, float]]
):
    """Test temperature and composition limits."""
    model = ThibodeauIDBinary(bff=bff)
    result = model.calculate(T=temperature, x=composition)

    comp_list = list(composition.keys())

    for comp in comp_list:
        assert result[comp] > 0


# tests that should fail
@pytest.mark.parametrize("temperature, composition, bff", binary_error_test_inputs)
def test_thibodeau_binary_id_errors(
    temperature: float, composition: dict[str, float], bff: Callable[[float, float, dict[str, float]], dict[str, float]]
):
    """Test if invalid inputs will fail."""
    model = ThibodeauIDBinary(bff=bff)
    with pytest.raises(ValueError):
        model.calculate(T=temperature, x=composition)


def test_loaded_parameters():
    """Test if parameters loads normally."""
    model = ThibodeauIDBinary(bff=dummy_bff)

    assert model.property == "Diffusivity"
    assert model.symbol == "D"
    assert model.display_symbol == "D"
    assert model.units == "\\meter\\squared\\per\\second"
    assert model.material == "Slag"
    assert model.references == ["thibodeau2016-ec"]

    assert model.bff == dummy_bff
    assert sorted(model.compound_scope) == ["Al2O3", "CaO", "MgO", "SiO2"]


def test_abstract_calc():
    """Test if calling the calculate() method implicitly works correctly."""
    model = ThibodeauIDBinary(bff=dummy_bff)
    composition = {"SiO2": 0.5, "Al2O3": 0.5}

    result1 = model.calculate(T=1700, x=composition)
    result2 = model(T=1700, x=composition)

    comp_list = list(composition.keys())

    for comp in comp_list:
        assert abs(result1[comp] - result2[comp]) < 1e-9
