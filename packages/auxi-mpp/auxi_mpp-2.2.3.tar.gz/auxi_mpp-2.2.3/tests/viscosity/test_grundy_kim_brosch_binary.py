"""Test GrundyKimBroschBinary model."""

from collections.abc import Callable

import pytest

from auxi.mpp.slag.μ._grundy_kim_brosch_binary import GrundyKimBroschBinary

from ..test_parameters._binary_testing_inputs import binary_error_test_inputs, binary_testing_inputs
from ..test_parameters._dummy_bff import dummy_bff


# tests that should pass
@pytest.mark.parametrize("temperature, composition, bff", binary_testing_inputs)
def test_grundy_kim_brosch_binary(
    temperature: float, composition: dict[str, float], bff: Callable[[float, float, dict[str, float]], dict[str, float]]
):
    """Test temperature and composition limits."""
    model = GrundyKimBroschBinary(bff=bff)
    result = model.calculate(T=temperature, x=composition)

    assert result > 0


# tests that should fail
@pytest.mark.parametrize("temperature, composition, bff", binary_error_test_inputs)
def test_grundy_kim_brosch_binary_errors(
    temperature: float, composition: dict[str, float], bff: Callable[[float, float, dict[str, float]], dict[str, float]]
):
    """Test if invalid inputs will fail."""
    model = GrundyKimBroschBinary(bff=bff)
    with pytest.raises(ValueError):
        model.calculate(T=temperature, x=composition)


def test_loaded_parameters():
    """Test if parameters loads normally."""
    model = GrundyKimBroschBinary(bff=dummy_bff)

    assert model.property == "Dynamic Viscosity"
    assert model.symbol == "μ"
    assert model.display_symbol == "\\mu"
    assert model.units == "\\pascal\\second"
    assert model.material == "Slag"
    assert model.references == ["grundy2008-part1", "grundy2008-part2", "kim2012-part3"]

    assert model.bff == dummy_bff
    assert model.names["AlO15"] == "Al2O3"
    assert model.cation["SiO2"] == "Si"
    assert model.struc_unit["Al2O3"] == "AlO15"
    assert model.struc_ox_count["CaO"] == 1
    assert model.parameters["MgO"]["A"] == -10.58
    assert model.cation_count["Al2O3"] == 2
    assert sorted(model.compound_scope) == ["Al2O3", "CaO", "MgO", "SiO2"]

    model.calculate(T=1700, x={"SiO2": 0.5, "Al2O3": 0.5})

    assert sorted(list(model.structural_x.keys())) == ["AlO15", "SiO2"]


def test_abstract_calc():
    """Test if calling the calculate() method implicitly works correctly."""
    model = GrundyKimBroschBinary(bff=dummy_bff)
    result1 = model.calculate(T=1700, x={"SiO2": 0.5, "Al2O3": 0.5})
    result2 = model(T=1700, x={"SiO2": 0.5, "Al2O3": 0.5})

    assert abs(result1 - result2) < 1e-9


def test_normalise_fractions():
    """Test if the function normalises."""
    model = GrundyKimBroschBinary(bff=dummy_bff)

    composition = {"SiO2": 2, "Al2O3": 2}
    normalised_comp = model._normalise_fractions(composition)  # type: ignore
    assert abs(normalised_comp["SiO2"] - 0.5) < 1e-9

    composition = {"SiO2": 0.1, "MgO": 0.6, "Al2O3": 0.1}
    normalised_comp = model._normalise_fractions(composition)  # type: ignore
    assert abs(normalised_comp["MgO"] - 0.75) < 1e-9


def test_count_oxygens():
    """Test if the oxygens per mole is counted correctly."""
    model = GrundyKimBroschBinary(bff=dummy_bff)

    n_oxygens = model._count_oxygens({"SiO2": 0.5, "AlO15": 0.5})  # type: ignore

    assert n_oxygens == 1.75
