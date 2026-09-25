"""Source model for client data retrieved from the ACA system."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ACAClient:
    """Represent an ACA client and the source metadata available for mapping."""

    client_id: str
    name: str
    metadata: dict[str, Any] = field(default_factory=dict)
