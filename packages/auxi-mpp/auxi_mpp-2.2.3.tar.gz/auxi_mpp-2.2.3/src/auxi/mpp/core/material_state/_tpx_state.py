from typing import Self

from pydantic import Field, model_validator

from auxi.chemistry.validation import listCompoundFormulas
from auxi.core.validation import floatFraction, floatPositive

from ._material_state import MaterialState


class TpxState(MaterialState):
    """
    Temperature and composition state for a material.

    Args:
    ----
        T : [K] Temperature.
        p : [Pa] Pressure.
        x : Mole fraction of material components.
    """

    T: floatPositive
    p: floatPositive
    x: dict[str, floatFraction]
    compounds: listCompoundFormulas = Field(default_factory=list)

    @model_validator(mode="after")
    def check_model(self) -> Self:
        self.compounds = list(self.x.keys())

        if self.T < 1000 or self.T > 2500:
            raise ValueError("Temperature should be above 1000 K and below 2500 K.")

        total_mole_frac = 0
        for comp in self.x:
            total_mole_frac += self.x[comp]
        if total_mole_frac != 1.00:
            raise ValueError("Mole fractions should add up to 1.00.")

        return self

    def _init(self):
        return
