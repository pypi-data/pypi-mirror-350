from auxi.chemistry.validation import dictChemicalCompositionBinary
from auxi.core.validation import floatPositive

from ._material_state import MaterialState


class TxBinaryState(MaterialState):
    """
    Temperature and composition state for a binary material.

    Args:
    ----
        T : [K] Temperature.
        x : Mole fraction of binary material components.
    """

    T: floatPositive
    x: dictChemicalCompositionBinary

    def _init(self):
        return
