"""Map ACA client records into the Client Complexity model."""

from collections.abc import Mapping

from models import ACAClient, ClientComplexity


def map_aca_client(
    client: ACAClient,
    field_mapping: Mapping[str, str],
) -> ClientComplexity:
    """Map selected ACA metadata keys to Client Complexity field names.

    ``field_mapping`` uses ACA metadata keys as keys and Client Complexity
    field names as values. Missing optional metadata is ignored.
    """

    mapped_fields = {
        destination: client.metadata[source]
        for source, destination in field_mapping.items()
        if source in client.metadata
    }

    return ClientComplexity(
        aca_client_id=client.client_id,
        client_name=client.name,
        fields=mapped_fields,
    )
