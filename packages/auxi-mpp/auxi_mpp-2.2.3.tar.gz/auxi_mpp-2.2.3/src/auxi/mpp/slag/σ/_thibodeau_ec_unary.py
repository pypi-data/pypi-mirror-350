from typing import Any, ClassVar

from pydantic import Field

from auxi.chemistry.validation import strCompoundFormula
from auxi.core.physicalconstants import F, R
from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from ...core.material_state import TpxState
from ..D import ThibodeauIDUnary
from ..Vm import ThibodeauUnary
from ._model import Model


class ThibodeauECUnary(Model[floatPositiveOrZero, floatPositiveOrZero, dict[str, floatFraction]]):
    """
    Unary liquid oxide electrical conductivity model by Thibodeau.

    Raises
    ------
        ValueError: If the provided compound formula is not found in the model's .yaml data file.

    Returns
    -------
       Electrical conductivity in [S/m].

    References
    ----------
        thibodeau2016-ec
    """

    data: ClassVar[dict[str, dict[str, floatPositiveOrZero]]] = {}

    references: ClassVar[list[strNotEmpty]] = ["thibodeau2016-ec"]
    compound_scope: list[strCompoundFormula] = Field(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

        self.compound_scope = list(self.data.keys())

    def calculate(
        self, T: floatPositiveOrZero = 298.15, p: floatPositiveOrZero = 101325, x: dict[str, floatFraction] = {}
    ) -> float:
        data = ThibodeauECUnary.data

        # validate T input
        state = TpxState(T=T, p=p, x=x)

        # ensure only one compound is given
        compound = list(x.keys())
        if len(compound) > 1:
            raise ValueError("Only one compound should be specified.")
        compound = compound[0]

        if compound not in self.compound_scope:
            raise ValueError(f"{compound} is not a valid formula. Valid options are '{' '.join(self.compound_scope)}'.")

        melt_Vm_object = ThibodeauUnary()
        Vm = melt_Vm_object.calculate(T=T, x=x)

        # convert to m^3/mol to cm^3/umol
        Vm = Vm / 1e-6

        # eqn 7
        D_dict: dict[str, float] = ThibodeauIDUnary().calculate(T=state.T, x=x)

        # eqn 8
        sigma = (
            100
            * ((data[compound]["z"] ** 2 * F**2) * (data[compound]["num_cats"]) * D_dict[compound])
            / ((R * state.T) * Vm)
        )

        return sigma


ThibodeauECUnary.load_data()
