"""
In-memory secrets store for HF Spaces and other read-only environments.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Dict, Optional

from pydantic import SecretStr

from openhands.core.config.openhands_config import OpenHandsConfig
from openhands.core.logger import openhands_logger as logger
from openhands.integrations.provider import CustomSecret, ProviderToken
from openhands.integrations.service_types import ProviderType
from openhands.storage.data_models.user_secrets import UserSecrets
from openhands.storage.secrets.secrets_store import SecretsStore


@dataclass
class MemorySecretsStore(SecretsStore):
    """
    In-memory secrets store that doesn't persist to disk.
    Perfect for HF Spaces and other read-only environments.
    
    Automatically loads secrets from environment variables.
    """
    _storage: Dict[str, UserSecrets] = field(default_factory=dict)
    user_id: str = "default"

    def _get_default_secrets(self) -> UserSecrets:
        """Get default secrets from environment variables."""
        try:
            provider_tokens = {}
            custom_secrets = {}
            
            # Load GitHub token if available
            github_token = os.getenv("GITHUB_TOKEN")
            if github_token:
                provider_tokens[ProviderType.GITHUB] = ProviderToken(
                    token=SecretStr(github_token),
                    host="github.com",
                    user_id=None
                )
                logger.info("Loaded GitHub token from environment")
            
            # Load GitLab token if available
            gitlab_token = os.getenv("GITLAB_TOKEN")
            if gitlab_token:
                provider_tokens[ProviderType.GITLAB] = ProviderToken(
                    token=SecretStr(gitlab_token),
                    host="gitlab.com",
                    user_id=None
                )
                logger.info("Loaded GitLab token from environment")
            
            # Load custom secrets from environment
            # Look for variables with specific prefixes
            custom_secret_prefixes = ["CUSTOM_SECRET_", "SECRET_"]
            for key, value in os.environ.items():
                for prefix in custom_secret_prefixes:
                    if key.startswith(prefix) and value:
                        secret_name = key[len(prefix):].lower()
                        custom_secrets[secret_name] = CustomSecret(
                            secret=SecretStr(value),
                            description=f"Custom secret loaded from {key}"
                        )
                        logger.info(f"Loaded custom secret: {secret_name}")
                        break
            
            # Also load common API keys as custom secrets
            api_key_mappings = {
                "OPENROUTER_API_KEY": "openrouter_api_key",
                "LLM_API_KEY": "llm_api_key", 
                "SEARCH_API_KEY": "search_api_key",
                "ANTHROPIC_API_KEY": "anthropic_api_key",
                "OPENAI_API_KEY": "openai_api_key",
            }
            
            for env_key, secret_name in api_key_mappings.items():
                value = os.getenv(env_key)
                if value:
                    custom_secrets[secret_name] = CustomSecret(
                        secret=SecretStr(value),
                        description=f"API key loaded from {env_key}"
                    )
                    logger.info(f"Loaded API key: {secret_name}")
            
            return UserSecrets(
                provider_tokens=MappingProxyType(provider_tokens),
                custom_secrets=MappingProxyType(custom_secrets)
            )
        except Exception as e:
            logger.error(f"Error creating default secrets: {e}")
            return UserSecrets()

    async def load(self) -> UserSecrets | None:
        """Load secrets from memory, auto-load from environment if none exist."""
        try:
            stored_secrets = self._storage.get(self.user_id)
            if stored_secrets is None:
                logger.info(f"No stored secrets found for user {self.user_id}, loading from environment")
                # Load default secrets from environment
                default_secrets = self._get_default_secrets()
                # Auto-store default secrets
                self._storage[self.user_id] = default_secrets
                logger.info(f"Default secrets loaded and stored for user {self.user_id}")
                return default_secrets
            
            logger.debug(f"Loaded existing secrets for user {self.user_id}")
            return stored_secrets
        except Exception as e:
            logger.error(f"Error loading secrets for user {self.user_id}: {e}")
            # Return empty secrets on error
            return UserSecrets()

    async def store(self, secrets: UserSecrets) -> None:
        """Store secrets in memory."""
        try:
            if not isinstance(secrets, UserSecrets):
                raise ValueError(f"Expected UserSecrets object, got {type(secrets)}")
            
            self._storage[self.user_id] = secrets
            logger.info(f"Secrets stored successfully for user {self.user_id}")
        except Exception as e:
            logger.error(f"Error storing secrets for user {self.user_id}: {e}")
            raise

    @classmethod
    async def get_instance(
        cls, config: OpenHandsConfig, user_id: str | None
    ) -> MemorySecretsStore:
        """Get instance of memory secrets store."""
        try:
            instance = MemorySecretsStore(user_id=user_id or "default")
            logger.info(f"Created MemorySecretsStore instance for user {instance.user_id}")
            return instance
        except Exception as e:
            logger.error(f"Error creating MemorySecretsStore instance: {e}")
            raise