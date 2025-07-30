"""
Settings for the agent_utils package.

This module contains the settings for the agent_utils package.

The settings are loaded from the environment variables.

TODO: Use credential files instead of environment variables, for managing multiple accounts or deployments.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from util_common.pydantic_util import show_settings_as_env


class ProxySettings(BaseSettings):
    """Proxy configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="PROXY_",
    )

    enabled: bool = Field(default=False, description="Whether to use proxy")
    url: str = Field(default="http://127.0.0.1:7891", description="Proxy URL")


class OpenAISettings(BaseSettings):
    """OpenAI configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="OPENAI_",
    )

    base_url: str = Field(default="https://api.openai.com/v1")
    api_key: str = Field(default="Please provide an API key")


class AzureOpenAISettings(BaseSettings):
    """Azure OpenAI configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="AZURE_OPENAI_",
    )

    base_url: str = Field(default="Please provide a base URL")
    api_key: str = Field(default="Please provide an API key")
    api_version: str = Field(default="2024-12-01-preview")
    gpt_4o_endpoint: str = Field(default="gpt-4o")
    o4_mini_endpoint: str = Field(default="o4-mini")
    embedding_3_small_endpoint: str = Field(default="text-embedding-3-small")


class ArkSettings(BaseSettings):
    """Ark configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="ARK_",
    )

    base_url: str = Field(default="https://ark.cn-beijing.volces.com/api/v3")
    api_key: str = Field(default="Please provide an API key")
    deepseek_r1_endpoint: str = Field(default="ep-20250409130925-m4htb")
    doubao_1_5_vision_pro_endpoint: str = Field(default="ep-20250421194416-l6m7c")
    doubao_1_5_thinking_pro_endpoint: str = Field(default="ep-20250421194823-f6wjb")


class VertexSettings(BaseSettings):
    """Google Vertex configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="VERTEX_",
    )

    credentials_path: Path = Field(
        default=Path("credentials/google-vertex.json"),
        description="Path to the Google service account credentials JSON file",
    )

    @property
    def service_account_info(self) -> dict:
        """Load service account info from the credentials JSON file."""
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"Google service account credentials file not found at {self.credentials_path}"
            )

        import json

        with open(self.credentials_path) as f:
            return json.load(f)


class AgentSettings(BaseSettings):
    """Main settings class that combines all settings."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="allow",
    )

    proxy: ProxySettings = Field(default_factory=ProxySettings)
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    azure_openai: AzureOpenAISettings = Field(default_factory=AzureOpenAISettings)
    ark: ArkSettings = Field(default_factory=ArkSettings)
    vertex: VertexSettings = Field(default_factory=VertexSettings)


# TODO: parse to params instead of call directly.
agent_settings = AgentSettings()
show_settings_as_env(agent_settings)
