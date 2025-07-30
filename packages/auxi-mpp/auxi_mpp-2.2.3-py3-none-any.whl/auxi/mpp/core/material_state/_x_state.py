from auxi.chemistry.validation import dictChemicalComposition

from ._material_state import MaterialState


class xState(MaterialState):
    """
    Composition state for a material.

    Args:
    ----
        x : Mole fraction of material components.
    """

    x: dictChemicalComposition

    def _init(self):
        return
