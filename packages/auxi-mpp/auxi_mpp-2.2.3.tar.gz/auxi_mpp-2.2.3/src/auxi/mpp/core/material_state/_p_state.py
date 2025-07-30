from auxi.core.validation import floatPositive

from ._material_state import MaterialState


class pState(MaterialState):
    """
    Pressure state for a material.

    Args:
    ----
        p : [Pa] Pressure.
    """

    p: floatPositive

    def _init(self):
        return
