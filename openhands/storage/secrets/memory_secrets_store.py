"""
In-memory secrets store for HF Spaces and other read-only environments.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from openhands.core.config.openhands_config import OpenHandsConfig
from openhands.storage.data_models.user_secrets import UserSecrets
from openhands.storage.secrets.secrets_store import SecretsStore


@dataclass
class MemorySecretsStore(SecretsStore):
    """
    In-memory secrets store that doesn't persist to disk.
    Perfect for HF Spaces and other read-only environments.
    """
    _storage: Dict[str, UserSecrets] = field(default_factory=dict)
    user_id: str = "default"

    async def load(self) -> UserSecrets | None:
        """Load secrets from memory."""
        return self._storage.get(self.user_id)

    async def store(self, secrets: UserSecrets) -> None:
        """Store secrets in memory."""
        self._storage[self.user_id] = secrets

    @classmethod
    async def get_instance(
        cls, config: OpenHandsConfig, user_id: str | None
    ) -> MemorySecretsStore:
        """Get instance of memory secrets store."""
        return MemorySecretsStore(user_id=user_id or "default")