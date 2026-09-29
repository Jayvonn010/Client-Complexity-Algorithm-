"""Validate ACA client data before it is mapped or scored."""

from collections.abc import Iterable

import pandas as pd


class ACAValidationError(ValueError):
    """Raised when ACA client data does not satisfy the input contract."""


class ACAValidator:
    """Validate required headers and client identity values."""

    DEFAULT_REQUIRED_HEADERS = ("Client Number", "Company Name")

    def __init__(self, required_headers: Iterable[str] | None = None) -> None:
        headers = required_headers or self.DEFAULT_REQUIRED_HEADERS
        self.required_headers = tuple(headers)

    def validate(self, dataframe: pd.DataFrame) -> None:
        """Raise ``ACAValidationError`` when the data is not usable."""

        self._validate_headers(dataframe)

        if dataframe.empty:
            raise ACAValidationError("ACA data contains no client records.")

        self._validate_required_values(dataframe)
        self._validate_unique_client_numbers(dataframe)

    def _validate_headers(self, dataframe: pd.DataFrame) -> None:
        missing_headers = [
            header
            for header in self.required_headers
            if header not in dataframe.columns
        ]

        if missing_headers:
            missing = ", ".join(missing_headers)
            raise ACAValidationError(f"Missing required headers: {missing}")

    def _validate_required_values(self, dataframe: pd.DataFrame) -> None:
        for header in self.required_headers:
            values = dataframe[header]
            blank_values = values.isna() | values.astype("string").str.strip().eq("")

            if blank_values.any():
                rows = [
                    str(position + 2)
                    for position, is_blank in enumerate(blank_values)
                    if is_blank
                ]
                raise ACAValidationError(
                    f"Required field '{header}' is blank on file row(s): "
                    f"{', '.join(rows)}"
                )

    @staticmethod
    def _validate_unique_client_numbers(dataframe: pd.DataFrame) -> None:
        duplicate_rows = dataframe["Client Number"].duplicated(keep=False)

        if duplicate_rows.any():
            duplicate_values = (
                dataframe.loc[duplicate_rows, "Client Number"]
                .astype("string")
                .drop_duplicates()
                .tolist()
            )
            duplicates = ", ".join(duplicate_values)
            raise ACAValidationError(
                f"Duplicate Client Number value(s): {duplicates}"
            )
