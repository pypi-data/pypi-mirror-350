"""Slag diffusivity models."""

from ._model import Model
from ._thibodeau_id_binary import ThibodeauIDBinary
from ._thibodeau_id_multi import ThibodeauIDMulti
from ._thibodeau_id_unary import ThibodeauIDUnary


__all__ = ["Model", "ThibodeauIDBinary", "ThibodeauIDMulti", "ThibodeauIDUnary"]
