"""Test ThibodeauIDUnary model."""

import pytest

from auxi.mpp.slag.D._thibodeau_id_unary import ThibodeauIDUnary

from ..test_parameters._unary_testing_inputs import unary_error_test_inputs, unary_testing_inputs


@pytest.mark.parametrize(
    "temperature, composition",
    unary_testing_inputs,
)
def test_thibodeau_id_unary(temperature: float, composition: dict[str, float]):
    """Test temperature limits."""
    model = ThibodeauIDUnary()
    result = model.calculate(T=temperature, x=composition)

    comp_list = list(composition.keys())

    for comp in comp_list:
        assert result[comp] > 0


# tests that should fail
@pytest.mark.parametrize("temperature, composition", unary_error_test_inputs)
def test_thibodeau_id_unary_errors(temperature: float, composition: dict[str, float]):
    """Test if invalid inputs will fail."""
    model = ThibodeauIDUnary()
    with pytest.raises(ValueError):
        model.calculate(T=temperature, x=composition)


def test_loaded_parameters():
    """Test if parameters loads normally."""
    model = ThibodeauIDUnary()

    assert model.property == "Diffusivity"
    assert model.symbol == "D"
    assert model.display_symbol == "D"
    assert model.units == "\\meter\\squared\\per\\second"
    assert model.material == "Slag"
    assert model.references == ["thibodeau2016-ec"]

    assert sorted(model.compound_scope) == ["Al2O3", "CaO", "MgO", "SiO2"]


def test_abstract_calc():
    """Test if calling the calculate() method works correctly."""
    model = ThibodeauIDUnary()
    result1 = model.calculate(T=1700, x={"SiO2": 1.0})
    result2 = model(T=1700, x={"SiO2": 1.0})

    comp_list = list({"SiO2": 1.0}.keys())

    for comp in comp_list:
        assert abs(result1[comp] - result2[comp]) < 1e-9
