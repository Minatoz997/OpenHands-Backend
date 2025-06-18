"""
In-memory settings store for HF Spaces and other read-only environments.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, Optional

from pydantic import SecretStr

from openhands.core.config.openhands_config import OpenHandsConfig
from openhands.core.logger import openhands_logger as logger
from openhands.storage.data_models.settings import Settings
from openhands.storage.data_models.user_secrets import UserSecrets
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
        try:
            # Check for API keys in environment variables
            openrouter_key = os.getenv("OPENROUTER_API_KEY")
            llm_api_key = os.getenv("LLM_API_KEY") or openrouter_key
            search_api_key = os.getenv("SEARCH_API_KEY")
            
            # Convert to SecretStr if keys exist
            llm_secret = SecretStr(llm_api_key) if llm_api_key else None
            search_secret = SecretStr(search_api_key) if search_api_key else None
            
            logger.info("Creating default settings for memory store")
            
            return Settings(
                # Core LLM settings
                llm_model=os.getenv("DEFAULT_LLM_MODEL", "openrouter/anthropic/claude-3-haiku-20240307"),
                llm_base_url=os.getenv("DEFAULT_LLM_BASE_URL", "https://openrouter.ai/api/v1"),
                llm_api_key=llm_secret,
                
                # Agent and language settings
                agent=os.getenv("DEFAULT_AGENT", "CodeActAgent"),
                language=os.getenv("DEFAULT_LANGUAGE", "en"),
                
                # Security and confirmation settings
                confirmation_mode=os.getenv("CONFIRMATION_MODE", "false").lower() == "true",
                security_analyzer=os.getenv("SECURITY_ANALYZER", ""),
                
                # Iteration and budget limits
                max_iterations=int(os.getenv("MAX_ITERATIONS", "30")),
                remote_runtime_resource_factor=int(os.getenv("REMOTE_RUNTIME_RESOURCE_FACTOR", "1")),
                
                # Feature flags
                enable_default_condenser=os.getenv("ENABLE_DEFAULT_CONDENSER", "true").lower() == "true",
                enable_sound_notifications=os.getenv("ENABLE_SOUND_NOTIFICATIONS", "false").lower() == "true",
                enable_proactive_conversation_starters=os.getenv("ENABLE_PROACTIVE_CONVERSATION_STARTERS", "true").lower() == "true",
                
                # Analytics consent
                user_consents_to_analytics=None,  # Let user decide
                
                # Container images
                sandbox_base_container_image=os.getenv("SANDBOX_BASE_CONTAINER_IMAGE"),
                sandbox_runtime_container_image=os.getenv("SANDBOX_RUNTIME_CONTAINER_IMAGE"),
                
                # Search API
                search_api_key=search_secret,
                
                # User info
                email=os.getenv("USER_EMAIL"),
                email_verified=os.getenv("EMAIL_VERIFIED", "false").lower() == "true" if os.getenv("EMAIL_VERIFIED") else None,
                
                # MCP config (will be None by default)
                mcp_config=None,
                
                # Secrets store
                secrets_store=UserSecrets()
            )
        except Exception as e:
            logger.error(f"Error creating default settings: {e}")
            # Return minimal settings if there's an error
            return Settings(
                language="en",
                agent="CodeActAgent",
                max_iterations=30,
                confirmation_mode=False,
                enable_default_condenser=True,
                enable_sound_notifications=False,
                enable_proactive_conversation_starters=True,
                secrets_store=UserSecrets()
            )

    async def load(self) -> Settings | None:
        """Load settings from memory, return defaults if none exist."""
        try:
            stored_settings = self._storage.get(self.user_id)
            if stored_settings is None:
                logger.info(f"No stored settings found for user {self.user_id}, creating defaults")
                # Return default settings for first-time users
                default_settings = self._get_default_settings()
                # Auto-store default settings to avoid recreating them
                self._storage[self.user_id] = default_settings
                logger.info(f"Default settings created and stored for user {self.user_id}")
                return default_settings
            
            logger.debug(f"Loaded existing settings for user {self.user_id}")
            return stored_settings
        except Exception as e:
            logger.error(f"Error loading settings for user {self.user_id}: {e}")
            # Return minimal default settings on error
            return self._get_default_settings()

    async def store(self, settings: Settings) -> None:
        """Store settings in memory."""
        try:
            if not isinstance(settings, Settings):
                raise ValueError(f"Expected Settings object, got {type(settings)}")
            
            self._storage[self.user_id] = settings
            logger.info(f"Settings stored successfully for user {self.user_id}")
        except Exception as e:
            logger.error(f"Error storing settings for user {self.user_id}: {e}")
            raise

    @classmethod
    async def get_instance(
        cls, config: OpenHandsConfig, user_id: str | None
    ) -> MemorySettingsStore:
        """Get instance of memory settings store."""
        try:
            instance = MemorySettingsStore(user_id=user_id or "default")
            logger.info(f"Created MemorySettingsStore instance for user {instance.user_id}")
            return instance
        except Exception as e:
            logger.error(f"Error creating MemorySettingsStore instance: {e}")
            raise