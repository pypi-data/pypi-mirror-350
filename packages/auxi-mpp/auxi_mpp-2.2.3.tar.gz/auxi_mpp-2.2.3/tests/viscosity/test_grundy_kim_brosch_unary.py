"""Test GrundyKimBroschUnary model."""

import pytest

from auxi.mpp.slag.μ._grundy_kim_brosch_unary import GrundyKimBroschUnary

from ..test_parameters._unary_testing_inputs import unary_error_test_inputs, unary_testing_inputs


@pytest.mark.parametrize(
    "temperature, composition",
    unary_testing_inputs,
)
def test_grundy_kim_brosch_unary(temperature: float, composition: dict[str, float]):
    """Test temperature limits."""
    model = GrundyKimBroschUnary()
    result = model.calculate(T=temperature, x=composition)

    assert result > 0


# tests that should fail
@pytest.mark.parametrize("temperature, composition", unary_error_test_inputs)
def test_grundy_kim_brosch_unary_errors(temperature: float, composition: dict[str, float]):
    """Test if invalid inputs will fail."""
    model = GrundyKimBroschUnary()
    with pytest.raises(ValueError):
        model.calculate(T=temperature, x=composition)


def test_loaded_parameters():
    """Test if parameters loads normally."""
    model = GrundyKimBroschUnary()

    assert model.property == "Dynamic Viscosity"
    assert model.symbol == "μ"
    assert model.display_symbol == "\\mu"
    assert model.units == "\\pascal\\second"
    assert model.material == "Slag"
    assert model.references == ["grundy2008-part1"]

    assert model.parameters["SiO2"]["A_*"] == -10.56
    assert model.cation_count["Al2O3"] == 2
    assert sorted(model.compound_scope) == ["Al2O3", "CaO", "MgO", "SiO2"]


def test_abstract_calc():
    """Test if calling the calculate() method implicitly works correctly."""
    model = GrundyKimBroschUnary()
    result1 = model.calculate(T=1700, x={"SiO2": 1.0})
    result2 = model(T=1700, x={"SiO2": 1.0})

    assert abs(result1 - result2) < 1e-9
