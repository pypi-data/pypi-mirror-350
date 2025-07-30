from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from .._slag_property_model import SlagPropertyModel


class Model[T: floatPositiveOrZero, p: floatPositiveOrZero, x: dict[str, floatFraction]](SlagPropertyModel[T, p, x]):
    """
    Base class for all slag viscosity models.

    In all cases, viscosity is calculated in units of [Pa.s].
    """

    property: strNotEmpty = "Dynamic Viscosity"
    symbol: strNotEmpty = "μ"
    display_symbol: strNotEmpty = "\\mu"
    units: strNotEmpty = "\\pascal\\second"
