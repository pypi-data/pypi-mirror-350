from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from .._slag_component_property_model import SlagComponentPropertyModel


class Model[T: floatPositiveOrZero, p: floatPositiveOrZero, x: dict[str, floatFraction]](
    SlagComponentPropertyModel[T, p, x]
):
    """
    Base class for all slag diffusivity models.

    In all cases, diffusivity is calculated in units of [m2/s].
    """

    property: strNotEmpty = "Diffusivity"
    symbol: strNotEmpty = "D"
    display_symbol: strNotEmpty = "D"
    units: strNotEmpty = "\\meter\\squared\\per\\second"
