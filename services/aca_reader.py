"""Read ACA client data from supported file formats."""

from pathlib import Path

import pandas as pd

from services.aca_validator import ACAValidator


class ACAReader:
    """Read and validate ACA client data files."""

    def __init__(self, validator: ACAValidator | None = None) -> None:
        self.validator = validator or ACAValidator()

    def read_file(self, file_path: str | Path) -> pd.DataFrame:
        """Read and validate a supported ACA data file."""

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        readers = {
            ".csv": self.read_csv,
            ".xlsx": self.read_excel,
            ".json": self.read_json,
        }

        extension = path.suffix.lower()
        reader = readers.get(extension)

        if reader is None:
            supported = ", ".join(readers)
            raise ValueError(
                f"Unsupported file type '{extension}'. "
                f"Supported types: {supported}"
            )

        dataframe = reader(path)
        self.validator.validate(dataframe)
        return dataframe

    @staticmethod
    def read_csv(file_path: Path) -> pd.DataFrame:
        """Read a CSV file."""

        return pd.read_csv(file_path)

    @staticmethod
    def read_excel(file_path: Path) -> pd.DataFrame:
        """Read an Excel workbook."""

        return pd.read_excel(file_path)

    @staticmethod
    def read_json(file_path: Path) -> pd.DataFrame:
        """Read a JSON file."""

        return pd.read_json(file_path)
