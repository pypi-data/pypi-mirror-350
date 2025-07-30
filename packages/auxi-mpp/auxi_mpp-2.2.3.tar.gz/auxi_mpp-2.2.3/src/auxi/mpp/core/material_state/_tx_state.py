from typing import Self

from pydantic import Field, model_validator

from auxi.chemistry.validation import dictChemicalComposition, listCompoundFormulas
from auxi.core.validation import floatPositive

from ._material_state import MaterialState


class TxState(MaterialState):
    """
    Temperature and composition state for a material.

    Args:
    ----
        T : [K] Temperature.
        x : Mole fraction of material components.
    """

    T: floatPositive
    x: dictChemicalComposition
    compounds: listCompoundFormulas = Field(default_factory=list)

    @model_validator(mode="after")
    def check_model(self) -> Self:
        self.compounds = list(self.x.keys())

        return self

    def _init(self):
        return
