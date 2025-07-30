from typing import Any, Self

from pydantic import model_validator

from auxi.chemistry.validation import strCompoundFormula
from auxi.core.validation import floatFraction, floatPositiveOrZero

from ...core.material_state import MaterialState


class SilicateBinarySlagEquilibriumTpxState(MaterialState):
    """
    Generate a temperature and composition state for a binary silicate slag.

    Args:
    ----
        T : [K] Temperature.
        p : [Pa] Pressure.
        x : Mole fraction of slag components.

    Raises:
    ------
        ValueError: If SiO2 is not one of the two compounds.
        ValueError: If more than one compound is specified in addition to SiO2.
    """

    T: floatPositiveOrZero
    p: floatPositiveOrZero
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

        if self.T < 1000 or self.T > 2500:
            raise ValueError("Temperature should be above 1000 K and below 2500 K.")

        total_mole_frac = 0
        for comp in self.x:
            total_mole_frac += self.x[comp]
        if total_mole_frac != 1.00:
            raise ValueError("Mole fractions should add up to 1.00.")

        if self.x["SiO2"] == 0.0:
            raise ValueError("Mole fraction of SiO2 cannot be zero.")

        compounds.remove("SiO2")
        self.compound = compounds.pop()

        return self

    def _init(self):
        return
