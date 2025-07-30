from typing import Optional

from pipelex import log
from pipelex.cogt.exceptions import CogtError
from pipelex.tools.config.models import ConfigModel
from pipelex.tools.environment import EnvVarNotFoundError, get_required_env
from pipelex.tools.secrets.secrets_errors import SecretNotFoundError
from pipelex.tools.secrets.secrets_provider_abstract import SecretsProviderAbstract


class CustomOpenAICredentialsError(CogtError):
    pass


class CustomOpenAIConfig(ConfigModel):
    """Configuration for custom OpenAI-compatible endpoints (e.g., Ollama, LM Studio, etc.)"""

    base_url: str
    api_key: Optional[str] = None
    # Option to load API key from environment or secrets if needed
    api_key_env_var_name: Optional[str] = None
    api_key_secret_name: Optional[str] = None

    def get_api_key(self, secrets_provider: Optional[SecretsProviderAbstract] = None) -> Optional[str]:
        """Get API key if configured, otherwise return None for services that don't require authentication"""

        # If api_key is directly set, use it
        if self.api_key:
            log.debug("Using Custom OpenAI API key from config.")
            return self.api_key

        # Try to get from environment variable if configured
        if self.api_key_env_var_name:
            log.debug("Using Custom OpenAI API key from environment.")
            try:
                key_from_env = get_required_env(self.api_key_env_var_name)
                return key_from_env
            except EnvVarNotFoundError as exc:
                raise CustomOpenAICredentialsError(f"Error getting Custom OpenAI API key from environment: {exc}") from exc

        # Try to get from secrets provider if configured
        if self.api_key_secret_name and secrets_provider:
            log.verbose("Using Custom OpenAI API key from secrets provider.")
            try:
                key_from_secrets_provider = secrets_provider.get_secret(secret_id=self.api_key_secret_name)
                return key_from_secrets_provider
            except SecretNotFoundError as exc:
                raise CustomOpenAICredentialsError("Error getting Custom OpenAI API key from secrets provider.") from exc

        # No API key configured - return None (for services that don't require auth)
        log.debug("No Custom OpenAI API key configured - using None.")
        return None
