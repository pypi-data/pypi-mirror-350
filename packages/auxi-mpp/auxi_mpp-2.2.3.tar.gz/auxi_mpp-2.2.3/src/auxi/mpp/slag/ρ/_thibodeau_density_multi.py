from collections.abc import Callable
from typing import Any, ClassVar

from pydantic import Field

from auxi.chemistry.validation import strCompoundFormula
from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from ..state import SilicateSlagEquilibriumTpxState
from ..Vm import ThibodeauMulti
from ._model import Model


class ThibodeauDensityMulti(Model[floatPositiveOrZero, floatPositiveOrZero, dict[str, floatFraction]]):
    """
    Ternary silicate melt density model derived from Thibodeau's molar volume model.

    Args:
    ----
        bff : Bond fraction function with temperature, pressure and composition as input and returns dictionary of bond fractions.

    Raises:
    ------
        ValueError: If SiO2 is not specified.
        ValueError: If the provided compound formula is not found in the model's .yaml data file.

    Returns:
    -------
       Density in [kg/m³].

    References:
    ----------
        thibodeau2016-part2, thibodeau2016-part3
    """

    data: ClassVar[dict[str, dict[str, Any]]] = {}

    references: ClassVar[list[strNotEmpty]] = ["thibodeau2016-part2", "thibodeau2016-part3"]

    bff: Callable[[float, float, dict[str, float]], dict[str, float]]
    molar_mass: dict[str, float] = Field(default_factory=dict)
    compound_scope: list[strCompoundFormula] = Field(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

        data = ThibodeauDensityMulti.data

        self.compound_scope: list[strCompoundFormula] = [c for c in list(data.keys())]
        self.molar_mass: dict[str, float] = {c: data[c]["molar mass"] for c in self.compound_scope}

    def calculate(
        self, T: floatPositiveOrZero = 298.15, p: floatPositiveOrZero = 101325, x: dict[str, floatFraction] = {}
    ) -> float:
        # validate input
        state = SilicateSlagEquilibriumTpxState(T=T, p=p, x=x)
        for c in state.x:
            if c not in self.compound_scope:
                raise ValueError(f"{c} is not a valid formula. Valid options are '{' '.join(self.compound_scope)}'.")

        molar_volume_model = ThibodeauMulti(bff=self.bff)
        Vm = molar_volume_model.calculate(T=state.T, x=state.x)

        # calculate composition specific molar mass of the system
        weighted_molar_masses: float = float(sum([self.molar_mass[comp] * (state.x[comp]) for comp in state.x]))

        # scale to units of kg/m-3
        ρ = (weighted_molar_masses / Vm) * 1e-3

        return ρ


ThibodeauDensityMulti.load_data()
