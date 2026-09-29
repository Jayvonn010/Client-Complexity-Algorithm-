"""Tests for loading ACA client data files."""

import unittest
from pathlib import Path

from services.aca_reader import ACAReader


class ACAReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = ACAReader()
        self.fixtures = Path(__file__).parent / "fixtures"

    def test_reads_csv_file(self) -> None:
        result = self.reader.read_file(self.fixtures / "clients.csv")

        self._assert_two_clients(result)

    def test_reads_excel_file(self) -> None:
        result = self.reader.read_file(self.fixtures / "clients.xlsx")

        self._assert_two_clients(result)

    def test_reads_json_file(self) -> None:
        result = self.reader.read_file(self.fixtures / "clients.json")

        self._assert_two_clients(result)

    def _assert_two_clients(self, result) -> None:
        self.assertEqual(result.shape, (2, 2))
        self.assertEqual(result.columns.tolist(), ["Client Number", "Company Name"])
        self.assertEqual(result.loc[0, "Client Number"], 123)
        self.assertEqual(result.loc[0, "Company Name"], "Example Company")
        self.assertEqual(result.loc[1, "Client Number"], 456)
        self.assertEqual(result.loc[1, "Company Name"], "Another Company")

    def test_rejects_missing_file(self) -> None:
        missing_file = Path("missing-clients.csv")

        with self.assertRaisesRegex(FileNotFoundError, "File does not exist"):
            self.reader.read_file(missing_file)

    def test_rejects_directory_path(self) -> None:
        with self.assertRaisesRegex(ValueError, "Path is not a file"):
            self.reader.read_file(self.fixtures)

    def test_rejects_unsupported_extension(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported file type"):
            self.reader.read_file(self.fixtures / "clients.txt")


if __name__ == "__main__":
    unittest.main()
