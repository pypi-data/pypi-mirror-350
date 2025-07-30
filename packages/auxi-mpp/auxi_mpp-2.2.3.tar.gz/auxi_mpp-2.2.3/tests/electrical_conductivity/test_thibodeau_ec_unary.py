"""Test ThibodeauECUnary model."""

import pytest

from auxi.mpp.slag.σ._thibodeau_ec_unary import ThibodeauECUnary

from ..test_parameters._unary_testing_inputs import unary_error_test_inputs, unary_testing_inputs


@pytest.mark.parametrize(
    "temperature, composition",
    unary_testing_inputs,
)
def test_ec_thibodeau_unary(temperature: float, composition: dict[str, float]):
    """Test temperature limits."""
    model = ThibodeauECUnary()
    result = model.calculate(T=temperature, x=composition)

    assert result > 0


# tests that should fail
@pytest.mark.parametrize("temperature, composition", unary_error_test_inputs)
def test_ec_thibodeau_unary_errors(temperature: float, composition: dict[str, float]):
    """Test if invalid inputs will fail."""
    model = ThibodeauECUnary()
    with pytest.raises(ValueError):
        model.calculate(T=temperature, x=composition)


def test_loaded_parameters():
    """Test if parameters loads normally."""
    model = ThibodeauECUnary()

    assert model.property == "Electrical Conductivity"
    assert model.symbol == "σ"
    assert model.display_symbol == "\\sigma"
    assert model.units == "\\siemens\\per\\meter"
    assert model.material == "Slag"
    assert model.references == ["thibodeau2016-ec"]

    assert sorted(model.compound_scope) == ["Al2O3", "CaO", "MgO", "SiO2"]


def test_abstract_calc():
    """Test if calling the calculate() method implicitly works correctly."""
    model = ThibodeauECUnary()
    result1 = model.calculate(T=1700, x={"SiO2": 1.0})
    result2 = model(T=1700, x={"SiO2": 1.0})

    assert abs(result1 - result2) < 1e-9
