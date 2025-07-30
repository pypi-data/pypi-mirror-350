from typing import Any, Self

from pydantic import model_validator

from auxi.chemistry.validation import strCompoundFormula
from auxi.core.validation import floatFraction, floatPositiveOrZero

from ...core.material_state import MaterialState


class SilicateBinarySlagEquilibriumTxState(MaterialState):
    """
    Generate a temperature and composition state for a binary silicate slag.

    Args:
    ----
        T : [K] Temperature.
        x : Mole fraction of slag components.

    Raises:
    ------
        ValueError: If SiO2 is not one of the two compounds.
        ValueError: If more than one compound is specified in addition to SiO2.
    """

    T: floatPositiveOrZero
    x: dict[str, floatFraction]
    compound: strCompoundFormula = ""

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

    @model_validator(mode="after")
    def check_model(self) -> Self:
        compounds: set[str] = set(self.x.keys())

        if "SiO2" not in compounds:
            raise ValueError("SiO2 must be one of the two compounds.")

        if len(compounds) != 2:
            raise ValueError("Exactly one compound must be specified in addition to SiO2.")

        compounds.remove("SiO2")
        self.compound = compounds.pop()

        return self

    def _init(self):
        return
