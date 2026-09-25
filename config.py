"""Environment-based application configuration."""

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    """Configuration required to connect to the target ClickUp list."""

    clickup_api_token: str
    clickup_list_id: str

    @classmethod
    def from_environment(cls) -> "Settings":
        """Load ClickUp settings from environment variables."""

        return cls(
            clickup_api_token=os.environ["CLICKUP_API_TOKEN"],
            clickup_list_id=os.environ["CLICKUP_LIST_ID"],
        )
