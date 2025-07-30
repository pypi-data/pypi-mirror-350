import inspect
from abc import abstractmethod
from pathlib import Path
from typing import Any, ClassVar

import yaml
from pydantic import ConfigDict

from auxi.core.objects import Object
from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from ._material_type import MaterialType


class MaterialPropertyModel[T: floatPositiveOrZero, p: floatPositiveOrZero, x: dict[str, floatFraction]](Object):
    r"""
    Base class of models that describe the variation of a specific material physical property.

    :param material_type: the type of material being described
    :param material: the name of the material being described, e.g. "Air"
    :param property: the name of the property being described, e.g. "density"
    :param symbol: the symbol of the property being described, e.g. "ρ"
    :param display symbol: the LaTeX display symbol of the property being described, e.g. "\\rho"
    :param units: the units used to express the property, e.g. "kg/m3"
    :param references: a list of literature references on which this model implementation is based, e.g. ['lienhard2015', 'smith2006']
    :param datasets: a list of data sets on which this model implementation is based, e.g. ['dataset-air-lienhard2015.csv']
    """

    data: ClassVar[dict[str, Any]] = {}

    @classmethod
    def load_data(
        cls,
        path: Path | None = None,
    ) -> None:
        if len(cls.data) == 0:
            if path is None:
                path = Path(inspect.getfile(cls))
            cls.data = yaml.safe_load(path.with_suffix(".yaml").read_text())

    model_config = ConfigDict(
        validate_assignment=True,
    )

    material_type: MaterialType = MaterialType.UNKNOWN
    material: strNotEmpty = ""
    property: strNotEmpty = ""
    symbol: strNotEmpty = ""
    display_symbol: strNotEmpty = ""
    units: strNotEmpty = ""
    references: ClassVar[list[strNotEmpty]] = []
    datasets: ClassVar[list[strNotEmpty]] = []

    def model_post_init(self, __context: Any) -> None:
        return super().model_post_init(__context)

        self.allowed_compounds: list[str] = []

    @staticmethod
    def normalise_assay(x: dict[str, float]) -> dict[str, float]:
        total = sum(x.values())
        x = {key: x[key] / total for key in x.keys()}
        return x

    def __call__(self, T: T = 298.15, p: p = 101325, x: x = {}):
        """
        For details about this method, please refer to the calculate method.
        """
        return self.calculate(T, p, x)

    @abstractmethod
    def calculate(self, T: T, p: p, x: x) -> float:
        """
        Calculate the property.

        Args:
        ----
            T: System temperature.
            p: System pressure.
            x: Chemical composition dictionary.

        Returns:
        -------
            Material property value.
        """
        ...

    def _init(self):
        return
