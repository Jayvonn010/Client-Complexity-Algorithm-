"""Tests for validating ACA client data."""

import unittest

import pandas as pd

from services.aca_validator import ACAValidationError, ACAValidator


class ACAValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = ACAValidator()

    def test_accepts_valid_client_data(self) -> None:
        dataframe = pd.DataFrame(
            {
                "Client Number": [123, 456],
                "Company Name": ["Example Company", "Another Company"],
            }
        )

        self.validator.validate(dataframe)

    def test_rejects_missing_required_header(self) -> None:
        dataframe = pd.DataFrame({"Company Name": ["Example Company"]})

        with self.assertRaisesRegex(
            ACAValidationError,
            "Missing required headers: Client Number",
        ):
            self.validator.validate(dataframe)

    def test_rejects_empty_data(self) -> None:
        dataframe = pd.DataFrame(columns=["Client Number", "Company Name"])

        with self.assertRaisesRegex(ACAValidationError, "no client records"):
            self.validator.validate(dataframe)

    def test_rejects_blank_required_value(self) -> None:
        dataframe = pd.DataFrame(
            {
                "Client Number": [123],
                "Company Name": ["   "],
            }
        )

        with self.assertRaisesRegex(
            ACAValidationError,
            "Required field 'Company Name' is blank on file row\\(s\\): 2",
        ):
            self.validator.validate(dataframe)

    def test_rejects_duplicate_client_numbers(self) -> None:
        dataframe = pd.DataFrame(
            {
                "Client Number": [123, 123],
                "Company Name": ["Example Company", "Example Company"],
            }
        )

        with self.assertRaisesRegex(
            ACAValidationError,
            "Duplicate Client Number value\\(s\\): 123",
        ):
            self.validator.validate(dataframe)


if __name__ == "__main__":
    unittest.main()
