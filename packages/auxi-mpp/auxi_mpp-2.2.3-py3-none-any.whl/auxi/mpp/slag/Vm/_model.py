from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from .._slag_property_model import SlagPropertyModel


class Model[T: floatPositiveOrZero, p: floatPositiveOrZero, x: dict[str, floatFraction]](SlagPropertyModel[T, p, x]):
    """
    Base class for all slag molar volume models.

    In all cases, molar volume is calculated in units of [m³/mol].
    """

    property: strNotEmpty = "Molar Volume"
    symbol: strNotEmpty = "Vm"
    display_symbol: strNotEmpty = "\\bar{V}"
    units: strNotEmpty = "\\cubic\\meter\\per\\mol"
