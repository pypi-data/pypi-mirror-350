"""Test ThibodeauDensityBinary model."""

from collections.abc import Callable

import pytest

from auxi.mpp.slag.ρ._thibodeau_density_binary import ThibodeauDensityBinary

from ..test_parameters._binary_testing_inputs import binary_error_test_inputs, binary_testing_inputs
from ..test_parameters._dummy_bff import dummy_bff


# tests that should pass
@pytest.mark.parametrize("temperature, composition, bff", binary_testing_inputs)
def test_thibodeau_density_binary(
    temperature: float, composition: dict[str, float], bff: Callable[[float, float, dict[str, float]], dict[str, float]]
):
    """Test temperature and composition limits."""
    model = ThibodeauDensityBinary(bff=bff)
    result = model.calculate(T=temperature, x=composition)

    assert result > 0


# tests that should fail
@pytest.mark.parametrize("temperature, composition, bff", binary_error_test_inputs)
def test_thibodeau_density_binary_errors(
    temperature: float, composition: dict[str, float], bff: Callable[[float, float, dict[str, float]], dict[str, float]]
):
    """Test if invalid inputs will fail."""
    model = ThibodeauDensityBinary(bff=bff)
    with pytest.raises(ValueError):
        model.calculate(T=temperature, x=composition)


def test_loaded_parameters():
    """Test if parameters loads normally."""
    model = ThibodeauDensityBinary(bff=dummy_bff)

    assert model.property == "Density"
    assert model.symbol == "ρ"
    assert model.display_symbol == "\\rho"
    assert model.units == "\\kilo\\gram\\per\\cubic\\meter"
    assert model.material == "Slag"
    assert model.references == ["thibodeau2016-part1", "thibodeau2016-part2"]

    assert model.bff == dummy_bff
    assert model.molar_mass["SiO2"] == 60.08
    assert sorted(model.compound_scope) == ["Al2O3", "CaO", "MgO", "SiO2"]


def test_abstract_calc():
    """Test if calling the calculate() method implicitly works correctly."""
    model = ThibodeauDensityBinary(bff=dummy_bff)
    result1 = model.calculate(T=1700, x={"SiO2": 0.5, "Al2O3": 0.5})
    result2 = model(T=1700, x={"SiO2": 0.5, "Al2O3": 0.5})

    assert abs(result1 - result2) < 1e-9
