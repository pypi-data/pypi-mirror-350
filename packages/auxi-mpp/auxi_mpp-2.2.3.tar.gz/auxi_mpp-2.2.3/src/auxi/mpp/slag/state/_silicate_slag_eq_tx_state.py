from typing import Any, Self

from pydantic import Field, model_validator

from auxi.chemistry.validation import listCompoundFormulas
from auxi.core.validation import floatFraction, floatPositiveOrZero

from ...core.material_state import MaterialState


class SilicateSlagEquilibriumTxState(MaterialState):
    """
    Generate a temperature and composition state for a multi-component silicate slag.

    Args:
    ----
        T : [K] Temperature.
        x : Mole fraction of slag components.

    Raises:
    ------
        ValueError: If SiO2 is not one of the compounds.
        ValueError: If less than 2 components is specified.
    """

    T: floatPositiveOrZero
    x: dict[str, floatFraction]
    compounds: listCompoundFormulas = Field(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

    @model_validator(mode="after")
    def check_model(self) -> Self:
        compounds: set[str] = set(self.x.keys())
        self.compounds = list(compounds)

        if "SiO2" not in compounds:
            raise ValueError("SiO2 must be one of the compounds.")

        if len(compounds) < 2:
            raise ValueError("Two or more compounds must be specified.")

        return self

    def _init(self):
        return
