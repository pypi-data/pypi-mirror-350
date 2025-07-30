from auxi.core.validation import floatPositive

from ._material_state import MaterialState


class TState(MaterialState):
    """
    Temperature state for a material.

    Args:
    ----
        T : [K] Temperature.
    """

    T: floatPositive

    def _init(self):
        return
