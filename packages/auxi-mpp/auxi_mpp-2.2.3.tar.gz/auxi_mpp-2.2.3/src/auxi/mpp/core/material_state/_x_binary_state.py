from auxi.chemistry.validation import dictChemicalCompositionBinary

from ._material_state import MaterialState


class xBinaryState(MaterialState):
    """
    Composition state for a binary material.

    Args:
    ----
        x : Mole fraction of binary material components.
    """

    x: dictChemicalCompositionBinary

    def _init(self):
        return
