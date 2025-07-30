"""Test ThibodeauUnary model."""

import pytest

from auxi.mpp.slag.Vm._thibodeau_unary import ThibodeauUnary

from ..test_parameters._unary_testing_inputs import unary_error_test_inputs, unary_testing_inputs


@pytest.mark.parametrize(
    "temperature, composition",
    unary_testing_inputs,
)
def test_thibodeau_unary(temperature: float, composition: dict[str, float]):
    """Test temperature limits."""
    model = ThibodeauUnary()
    result = model.calculate(T=temperature, x=composition)

    assert result > 0


# tests that should fail
@pytest.mark.parametrize("temperature, composition", unary_error_test_inputs)
def test_thibodeau_unary_errors(temperature: float, composition: dict[str, float]):
    """Test if invalid inputs will fail."""
    model = ThibodeauUnary()
    with pytest.raises(ValueError):
        model.calculate(T=temperature, x=composition)


def test_loaded_parameters():
    """Test if parameters loads normally."""
    model = ThibodeauUnary()

    assert model.property == "Molar Volume"
    assert model.symbol == "Vm"
    assert model.display_symbol == "\\bar{V}"
    assert model.units == "\\cubic\\meter\\per\\mol"
    assert model.material == "Slag"
    assert model.references == ["thibodeau2016-part1"]

    assert sorted(model.compound_scope) == ["Al2O3", "CaO", "MgO", "SiO2"]

    model.calculate(T=1700, x={"SiO2": 1.0})

    assert model.a == 27.3
    assert model.b == 0.0
    assert model.oxygen_number == 2


def test_abstract_calc():
    """Test if calling the calculate() method works correctly."""
    model = ThibodeauUnary()
    result1 = model.calculate(T=1700, x={"SiO2": 1.0})
    result2 = model(T=1700, x={"SiO2": 1.0})

    assert abs(result1 - result2) < 1e-9
