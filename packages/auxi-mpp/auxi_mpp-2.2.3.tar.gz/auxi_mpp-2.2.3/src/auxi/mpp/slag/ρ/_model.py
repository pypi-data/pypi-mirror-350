from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from .._slag_property_model import SlagPropertyModel


class Model[T: floatPositiveOrZero, p: floatPositiveOrZero, x: dict[str, floatFraction]](SlagPropertyModel[T, p, x]):
    """
    Base class for all slag density models.

    In all cases, density is calculated in units of [kg/m³].
    """

    property: strNotEmpty = "Density"
    symbol: strNotEmpty = "ρ"
    display_symbol: strNotEmpty = "\\rho"
    units: strNotEmpty = "\\kilo\\gram\\per\\cubic\\meter"
