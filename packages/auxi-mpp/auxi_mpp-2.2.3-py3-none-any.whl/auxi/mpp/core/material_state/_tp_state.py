from auxi.core.validation import floatPositive

from ._material_state import MaterialState


class TpState(MaterialState):
    """
    Temperature and pressure state for a material.

    Args:
    ----
        T : [K] Temperature.
        p : [Pa] Pressure.
    """

    T: floatPositive
    p: floatPositive

    def _init(self):
        return
