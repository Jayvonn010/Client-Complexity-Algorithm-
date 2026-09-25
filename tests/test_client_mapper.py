"""Tests for mappings between ACA and Client Complexity records."""

import unittest

from models import ACAClient
from services.client_mapper import map_aca_client


class ClientMapperTests(unittest.TestCase):
    def test_maps_configured_metadata_fields(self) -> None:
        client = ACAClient(
            client_id="client-123",
            name="Example Client",
            metadata={"employee_count": 250, "ignored": "value"},
        )

        result = map_aca_client(client, {"employee_count": "number_of_people"})

        self.assertEqual(result.aca_client_id, "client-123")
        self.assertEqual(result.client_name, "Example Client")
        self.assertEqual(result.fields, {"number_of_people": 250})


if __name__ == "__main__":
    unittest.main()
