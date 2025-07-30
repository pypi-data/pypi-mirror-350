from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from .._slag_property_model import SlagPropertyModel


class Model[T: floatPositiveOrZero, p: floatPositiveOrZero, x: dict[str, floatFraction]](SlagPropertyModel[T, p, x]):
    """
    Base class for all slag electrical conductivity models.

    In all cases, electrical conductivity is calculated in units of [S/m].
    """

    property: strNotEmpty = "Electrical Conductivity"
    symbol: strNotEmpty = "σ"
    display_symbol: strNotEmpty = "\\sigma"
    units: strNotEmpty = "\\siemens\\per\\meter"
