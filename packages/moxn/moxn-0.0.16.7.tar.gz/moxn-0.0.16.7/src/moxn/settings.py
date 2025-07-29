from pydantic import HttpUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class MoxnSettings(BaseSettings):
    """Configuration settings for the Moxn client."""

    user_id: str
    org_id: str | None = None
    api_key: SecretStr
    base_api_route: HttpUrl = Field(
        default=HttpUrl("https://marksweissma--moxn-api-fastapi-app.modal.run")
    )
    timeout: float = Field(default=30.0, description="Prompt timeout in seconds")
    telemetry_timeout: float = Field(
        default=120.0, description="Telemetry timeout in seconds"
    )
    # Content refresh configuration
    content_refresh_cfg_concurrency: int = Field(
        default=4, description="Max concurrent refresh operations"
    )
    content_refresh_cfg_buffer: int = Field(
        default=300,
        description="Buffer time in seconds before expiry to trigger refresh",
    )
    content_refresh_cfg_tick: float = Field(
        default=60.0, description="Refresh check interval in seconds"
    )
    content_refresh_cfg_max_batch: int = Field(
        default=20, description="Maximum batch size for refreshes"
    )
    content_refresh_cfg_refresh_timeout: float = Field(
        default=30.0, description="Timeout for refresh operations in seconds"
    )
    content_refresh_cfg_min_refresh_interval: float = Field(
        default=1.0, description="Minimum seconds between refresh attempts"
    )

    model_config = SettingsConfigDict(
        frozen=True,
        extra="forbid",
        env_file=[".env.local", ".env"],
        env_prefix="MOXN_",
        env_file_encoding="utf-8",
    )


@lru_cache(maxsize=1)
def get_moxn_settings() -> MoxnSettings:
    return MoxnSettings()  # type: ignore
