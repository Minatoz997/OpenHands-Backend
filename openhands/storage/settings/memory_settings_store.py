"""
In-memory settings store for HF Spaces and other read-only environments.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, Optional

from openhands.core.config.openhands_config import OpenHandsConfig
from openhands.storage.data_models.settings import Settings
from openhands.storage.settings.settings_store import SettingsStore


@dataclass
class MemorySettingsStore(SettingsStore):
    """
    In-memory settings store that doesn't persist to disk.
    Perfect for HF Spaces and other read-only environments.
    """
    _storage: Dict[str, Settings] = field(default_factory=dict)
    user_id: str = "default"

    def _get_default_settings(self) -> Settings:
        """Get default settings pre-configured for easy use."""
        # Check if OpenRouter API key is available in environment
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        
        return Settings(
            llm_model=os.getenv("DEFAULT_LLM_MODEL", "openrouter/anthropic/claude-3-haiku-20240307"),
            llm_base_url=os.getenv("DEFAULT_LLM_BASE_URL", "https://openrouter.ai/api/v1"),
            llm_api_key=openrouter_key,  # Will be None if not set
            agent="CodeActAgent",
            language="en",
            confirmation_mode=False,
            security_analyzer="",
            enable_auto_lint=False,
            disable_color=False,
            llm_config={
                "model": os.getenv("DEFAULT_LLM_MODEL", "openrouter/anthropic/claude-3-haiku-20240307"),
                "base_url": os.getenv("DEFAULT_LLM_BASE_URL", "https://openrouter.ai/api/v1"),
                "api_key": openrouter_key
            }
        )

    async def load(self) -> Settings | None:
        """Load settings from memory, return defaults if none exist."""
        stored_settings = self._storage.get(self.user_id)
        if stored_settings is None:
            # Return default settings for first-time users
            default_settings = self._get_default_settings()
            # Only auto-store if we have an API key
            if default_settings.llm_api_key:
                self._storage[self.user_id] = default_settings
            return default_settings
        return stored_settings

    async def store(self, settings: Settings) -> None:
        """Store settings in memory."""
        self._storage[self.user_id] = settings

    @classmethod
    async def get_instance(
        cls, config: OpenHandsConfig, user_id: str | None
    ) -> MemorySettingsStore:
        """Get instance of memory settings store."""
        return MemorySettingsStore(user_id=user_id or "default")