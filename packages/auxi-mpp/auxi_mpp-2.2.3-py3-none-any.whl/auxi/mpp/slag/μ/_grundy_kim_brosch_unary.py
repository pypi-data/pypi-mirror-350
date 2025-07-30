import math
from typing import Any, ClassVar

from pydantic import Field

from auxi.chemistry.validation import strCompoundFormula
from auxi.core.physicalconstants import R
from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from ...core.material_state import TpxState
from ._model import Model


class GrundyKimBroschUnary(Model[floatPositiveOrZero, floatPositiveOrZero, dict[str, floatFraction]]):
    """
    Unary slag dynamic viscosity model by Grundy, Kim, and Brosch.

    Raises
    ------
        ValueError: If the compound formula is not found in the model's .yaml data file.

    Returns
    -------
       Dynamic viscosity in [Pa.s].

    References
    ----------
        grundy2008-part1
    """

    data: ClassVar[dict[str, dict[str, Any]]] = {}

    references: ClassVar[list[strNotEmpty]] = ["grundy2008-part1"]

    parameters: dict[str, dict[str, float]] = Field(default_factory=dict)
    cation_count: dict[str, int] = Field(default_factory=dict)
    compound_scope: list[strCompoundFormula] = Field(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

        data = GrundyKimBroschUnary.data
        self.compound_scope = list(self.data.keys())

        self.parameters: dict[str, dict[str, float]] = {c: data[c]["parameters"] for c in self.compound_scope}
        self.cation_count: dict[str, int] = {c: data[c]["cation_count"] for c in self.compound_scope}

    def calculate(
        self, T: floatPositiveOrZero = 298.15, p: floatPositiveOrZero = 101325, x: dict[str, floatFraction] = {}
    ) -> float:
        # validate state
        state = TpxState(T=T, p=p, x=x)

        # ensure only one compound is given
        compound = list(state.x.keys())
        if len(compound) > 1:
            raise ValueError("Only one compound should be specified.")
        compound = compound[0]

        # validate input
        if compound not in self.compound_scope:
            raise ValueError(f"{compound} is not a valid formula. Valid options are '{' '.join(self.compound_scope)}'.")

        # eqn 11
        if compound == "SiO2":
            A_param = self.parameters["SiO2"]["A_*"] + self.parameters["SiO2"]["A_E"]
            E_param = self.parameters["SiO2"]["E_*"] + self.parameters["SiO2"]["E_E"]

        else:
            A_param = self.parameters[compound]["A"]
            E_param = self.parameters[compound]["E"]

        # eqn 10
        mu = math.exp(A_param + E_param / (R * state.T))

        return mu


GrundyKimBroschUnary.load_data()
