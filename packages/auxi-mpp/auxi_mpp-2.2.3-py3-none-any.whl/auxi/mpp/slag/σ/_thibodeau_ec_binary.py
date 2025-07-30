from collections.abc import Callable
from typing import Any, ClassVar

from pydantic import Field

from auxi.chemistry.validation import strCompoundFormula
from auxi.core.physicalconstants import F, R
from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from ..D import ThibodeauIDBinary
from ..state import SilicateBinarySlagEquilibriumTpxState
from ..Vm import ThibodeauBinary
from ._model import Model


class ThibodeauECBinary(Model[floatPositiveOrZero, floatPositiveOrZero, dict[str, floatFraction]]):
    """
    Binary or multi-component silicate liquid oxide electrical conductivity model by Thibodeau.

    Args:
    ----
        bff : Bond fraction function with temperature, pressure and composition as input and returns dictionary of bond fractions.

    Raises:
    ------
        ValueError: If SiO2 is specified.
        ValueError: If the provided compound formula is not found in the model's .yaml data file.

    Returns:
    -------
       Electrical conductivity in [S/m].

    References:
    ----------
        thibodeau2016-ec
    """

    data: ClassVar[dict[str, dict[str, Any]]] = {}

    references: ClassVar[list[strNotEmpty]] = ["thibodeau2016-ec"]
    compound_scope: list[strCompoundFormula] = Field(default_factory=list)

    bff: Callable[[float, float, dict[str, float]], dict[str, float]]

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

        self.compound_scope = list(self.data.keys())

    def calculate(
        self, T: floatPositiveOrZero = 298.15, p: floatPositiveOrZero = 101325, x: dict[str, floatFraction] = {}
    ) -> float:
        # validate input
        state = SilicateBinarySlagEquilibriumTpxState(T=T, p=p, x=x)

        for c in state.x:
            if c not in self.compound_scope:
                raise ValueError(f"{c} is not a valid formula. Valid options are '{' '.join(self.compound_scope)}'.")

        data = ThibodeauECBinary.data

        # calculate the molar volume
        melt_Vm_object = ThibodeauBinary(bff=self.bff)
        Vm = melt_Vm_object.calculate(T=state.T, x=state.x)

        # convert to m^3/mol to cm^3/mol
        Vm = Vm / 1e-6

        # eqn 7 - calculate diffusivity for each cation
        D_dict: dict[str, float] = ThibodeauIDBinary(bff=self.bff).calculate(T=state.T, x=state.x)

        # eqn 8 - sum of all cation contributions to electrical conductivity
        sigma: float = 0.0
        for comp in state.x:
            sigma += (
                100
                * ((data[comp]["z"] ** 2 * F**2) * (data[comp]["num_cats"] * state.x[comp]) * D_dict[comp])
                / ((R * state.T) * Vm)
            )

        return sigma


ThibodeauECBinary.load_data()
