import csv
from pathlib import Path

import polars as pl


class Dataset:
    """
    Contains a dataset used to create and/or test a material physical property model.

    :param path: path to the .csv file that contains the data
    """

    @classmethod
    def create_template(cls, material: str, path: Path) -> Path:
        """
        Create a template csv file for a dataset.

        :param material: the name of the material
        :param path: the path of the directory where the file must be written
        :param show: a boolean indicating whether the created file should be displayed after creation
        """
        from shutil import copy

        file_name = f"dataset-{material.lower().replace(' ', '-')}.csv"
        file_path = path / file_name

        template_path = Path(__file__).with_suffix(".template.csv")

        if file_path.exists():
            raise FileExistsError(f"File '{file_path}' already exists.")

        copy(template_path, file_path)

        return file_path

    def __init__(self, path: Path):
        self._path: Path = path

        self._name: str = path.name
        self._material: str
        self._description: str
        self._reference: str
        self._col_names: dict[str, str]
        self._col_symbols: list[str]
        self._col_display_symbols: dict[str, str]
        self._col_units: dict[str, str]
        self._data: pl.DataFrame

        self._read_header_information()
        self._read_data()

    def __str__(self):
        result = "Material:         {self.material}\n"
        result += "Description:      {self.description}\n"
        result += "References:       {self.reference}\n"
        result += "Properties:       {self.col_names}\n"
        result += "Symbols:          {self.col_symbols}\n"
        result += "Display symbols:  {self.col_display_symbols}\n"
        result += "Units:            {self.col_units}\n"
        result += "Data:\n"
        result += str(self.data)

        return result

    @property
    def path(self) -> Path:
        """Dataset .csv file path."""
        return self._path

    @property
    def name(self) -> str:
        """Dataset name."""
        return self._name

    @property
    def material(self) -> str:
        """The name of the material represented by the dataset."""
        return self._material

    @property
    def description(self) -> str:
        """Dataset description."""
        return self._description

    @property
    def reference(self) -> str:
        """Dataset source reference."""
        return self._reference

    @property
    def col_names(self) -> dict[str, str]:
        """Dataset column names."""
        return self._col_names

    @property
    def col_symbols(self) -> list[str]:
        """Dataset column symbols."""
        return self._col_symbols

    @property
    def col_display_symbols(self) -> dict[str, str]:
        """Dataset column display symbols."""
        return self._col_display_symbols

    @property
    def col_units(self) -> dict[str, str]:
        """Dataset column units."""
        return self._col_units

    @property
    def data(self) -> pl.DataFrame:
        """The dataset as a polars DataFrame."""
        return self._data

    def _read_header_information(self):
        with open(self._path, newline="") as file:
            lines = csv.reader(file, delimiter=",", quotechar='"')

            self._material = next(lines)[1]
            self._description = next(lines)[1]
            self._reference = next(lines)[1]

            col_names = next(lines)
            col_units = next(lines)
            col_display_symbols = next(lines)
            self._col_symbols = next(lines)

        self._col_names = dict(zip(self._col_symbols, col_names))
        self._col_display_symbols = dict(zip(self._col_symbols, col_display_symbols))
        self._col_units = dict(zip(self._col_symbols, col_units))

    def _read_data(self):
        self._data: pl.DataFrame = pl.read_csv(self._path, skip_rows=6)

        # header: dict[
        #     str,
        #     str,
        # ] = {}
        # for symbol in self.col_symbols:
        #     header[symbol] = f"{symbol}[{self.col_units[symbol]}]"

        # self._data = self.data.rename(
        #     mapping=header,
        #     strict=True,
        # )
