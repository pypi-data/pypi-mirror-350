import math
from typing import Any, ClassVar

from pydantic import Field

from auxi.chemistry.validation import strCompoundFormula
from auxi.core.physicalconstants import R
from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from ...core.material_state import TpxState
from ._model import Model


class ThibodeauIDUnary(Model[floatPositiveOrZero, floatPositiveOrZero, dict[str, floatFraction]]):
    """
    Unary ionic diffusivity model by Thibodeau.

    Returns
    -------
       Dictionary containing the diffusivity of the cation in units of [m²/s].

    References
    ----------
        thibodeau2016-ec
    """

    references: ClassVar[list[strNotEmpty]] = ["thibodeau2016-ec"]
    compound_scope: list[strCompoundFormula] = Field(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

        data = ThibodeauIDUnary.data
        self.compound_scope = list(data.keys())

    def calculate(
        self, T: floatPositiveOrZero = 298.15, p: floatPositiveOrZero = 101325, x: dict[str, floatFraction] = {}
    ) -> dict[str, float]:
        data = ThibodeauIDUnary.data

        # validate input
        state = TpxState(T=T, p=p, x=x)

        # ensure only one compound is given
        compound = list(state.x.keys())
        if len(compound) > 1:
            raise ValueError("Only one compound should be specified.")
        compound = compound[0]

        # validate input
        if compound not in self.compound_scope:
            raise ValueError(f"{compound} is not a valid formula. Valid options are '{' '.join(self.compound_scope)}'.")

        # load A, B and C parameters for specified components
        A_param = data[compound]["param"]["A"]
        B_param = data[compound]["param"]["B"]
        D_comps: dict[str, float] = {}

        # equation 7 - calculate diffusivity for the cation
        D_i = A_param * math.exp(-(float(B_param)) / (R * state.T))

        D_comps[compound] = D_i

        return D_comps


ThibodeauIDUnary.load_data()
