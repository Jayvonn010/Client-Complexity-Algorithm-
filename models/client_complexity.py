"""Destination model for data that will be synchronized with ClickUp."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ClientComplexity:
    """Represent the mapped client data and calculated complexity values."""

    aca_client_id: str
    client_name: str
    fields: dict[str, Any] = field(default_factory=dict)
    clickup_task_id: str | None = None
