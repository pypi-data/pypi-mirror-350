import math
from collections.abc import Callable
from typing import Any, ClassVar

from pydantic import Field

from auxi.chemistry.validation import strCompoundFormula
from auxi.core.physicalconstants import R
from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from ..state import SilicateBinarySlagEquilibriumTpxState
from ._model import Model


class ThibodeauIDBinary(Model[floatPositiveOrZero, floatPositiveOrZero, dict[str, floatFraction]]):
    """
    Binary liquid silicate slag ionic diffusivity model by Thibodeau.

    Args:
    ----
        bff : Bond fraction function with temperature, pressure and composition as input and returns dictionary of bond fractions.

    Returns:
    -------
       Dictionary containing the diffusivity of each cation in units of [m²/s].

    References:
    ----------
        thibodeau2016-ec
    """

    references: ClassVar[list[strNotEmpty]] = ["thibodeau2016-ec"]
    compound_scope: list[strCompoundFormula] = Field(default_factory=list)

    bff: Callable[[float, float, dict[str, float]], dict[str, float]]

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

        data = ThibodeauIDBinary.data
        self.compound_scope = list(data.keys())

    def calculate(
        self, T: floatPositiveOrZero = 298.15, p: floatPositiveOrZero = 101325, x: dict[str, floatFraction] = {}
    ) -> dict[str, float]:
        data = ThibodeauIDBinary.data

        # validate input
        state = SilicateBinarySlagEquilibriumTpxState(T=T, p=p, x=x)
        for c in state.x:
            if c not in self.compound_scope:
                raise ValueError(f"{c} is not a valid formula. Valid options are '{' '.join(self.compound_scope)}'.")

        # load A, B and C parameters for specified components
        A_params = {c: data[c]["param"]["A"] for c in state.x}
        B_params = {c: data[c]["param"]["B"] for c in state.x}
        C_params = {c: data[c]["param"]["C"] for c in state.x}

        # get SiSi, SiAl and AlAl bond fractions
        x_b = self.bff(state.T, p, state.x)
        # assign zero for Al interactions if Al2O3 not present
        if "Al-Si" not in x_b:
            x_b["Al-Si"] = 0.0
            x_b["Al-Al"] = 0.0

        D_comps: dict[str, float] = {}

        # equation 7 - calculate diffusivity for each cation
        for comp in state.x:
            D_i = A_params[comp] * math.exp(
                -(
                    float(B_params[comp])
                    + (
                        float(C_params[comp]["C_SiSi"]) * float(x_b["Si-Si"])
                        + float(C_params[comp]["C_AlSi"]) * float(x_b["Al-Si"])
                        + float(C_params[comp]["C_AlAl"]) * float(x_b["Al-Al"])
                    )
                )
                / (R * state.T)
            )

            D_comps[comp] = D_i

        return D_comps


ThibodeauIDBinary.load_data()
