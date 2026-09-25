"""Create or update Client Complexity tasks in ClickUp."""

from models import ClientComplexity


class ClickUpSyncService:
    """Coordinate Client Complexity task upserts in ClickUp."""

    def __init__(self, api_token: str, list_id: str) -> None:
        self.api_token = api_token
        self.list_id = list_id

    def upsert_client(self, client: ClientComplexity) -> str:
        """Create or update a ClickUp task and return its task ID."""

        raise NotImplementedError(
            "ClickUp synchronization requires the final task and custom-field mapping."
        )
