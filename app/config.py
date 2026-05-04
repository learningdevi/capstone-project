from functools import lru_cache
from urllib.parse import urlparse

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    azure_openai_endpoint: str = Field(...)
    azure_openai_key: str = Field(...)
    azure_openai_api_version: str = "2025-04-01-preview"
    azure_openai_chat_deployment: str = "gpt-4o"
    azure_openai_judge_deployment: str = "gpt-4o"

    @property
    def endpoint_base(self) -> str:
        """Strip any /openai/deployments/... suffix and return scheme://host/."""
        parsed = urlparse(self.azure_openai_endpoint)
        return f"{parsed.scheme}://{parsed.netloc}/"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
