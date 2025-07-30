from collections.abc import Callable
from typing import Any, ClassVar

from pydantic import Field

from auxi.chemistry.validation import strCompoundFormula
from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from ..state import SilicateBinarySlagEquilibriumTpxState
from ..Vm import ThibodeauBinary
from ._model import Model


class ThibodeauDensityBinary(Model[floatPositiveOrZero, floatPositiveOrZero, dict[str, floatFraction]]):
    """
    Binary liquid silicate slag density model derived from Thibodeau's molar volume model.

    Args:
    ----
        bff : Bond fraction function with temperature, pressure and composition as input and returns dictionary of bond fractions.

    Raises:
    ------
        ValueError: If SiO2 is specified.
        ValueError: If the provided compound formula is not found in the model's .yaml data file.

    Returns:
    -------
       Density in [kg/m³].

    References:
    ----------
        thibodeau2016-part1, thibodeau2016-part2
    """

    data: ClassVar[dict[str, dict[str, Any]]] = {}

    references: ClassVar[list[strNotEmpty]] = ["thibodeau2016-part1", "thibodeau2016-part2"]

    bff: Callable[[float, float, dict[str, float]], dict[str, float]]
    molar_mass: dict[str, float] = Field(default_factory=dict)
    compound_scope: list[strCompoundFormula] = Field(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        data = ThibodeauDensityBinary.data

        self.compound_scope: list[strCompoundFormula] = [c for c in list(data.keys())]
        self.molar_mass: dict[str, float] = {c: data[c]["molar mass"] for c in self.compound_scope}

    def calculate(
        self, T: floatPositiveOrZero = 298.15, p: floatPositiveOrZero = 101325, x: dict[str, floatFraction] = {}
    ) -> float:
        # validate input
        state = SilicateBinarySlagEquilibriumTpxState(T=T, p=p, x=x)
        for c in state.x:
            if c not in self.compound_scope:
                raise ValueError(f"{c} is not a valid formula. Valid options are '{' '.join(self.compound_scope)}'.")

        molar_volume_model = ThibodeauBinary(bff=self.bff)
        Vm = molar_volume_model.calculate(T=state.T, x=state.x)

        # calculate composition specific molar mass of the system
        weighted_molar_masses: float = sum([self.molar_mass[comp] * (state.x[comp]) for comp in state.x])

        # scale to units of kg/m³
        ρ = (weighted_molar_masses / Vm) * 1e-3

        return ρ


ThibodeauDensityBinary.load_data()
