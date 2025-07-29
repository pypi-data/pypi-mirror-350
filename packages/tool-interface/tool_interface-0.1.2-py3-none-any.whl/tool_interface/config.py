from pathlib import Path
from functools import lru_cache
from typing import Any, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv(Path.cwd() / "default.env", override=False)
load_dotenv(Path.cwd() / ".env", override=False)


class Settings(BaseSettings):
    """Main settings for tool-interface."""

    # Supabase settings
    supabase_url: str = ""
    supabase_key: str = ""

    # Storage settings (S3 compatible)
    storage_endpoint_url: Optional[str] = None
    storage_access_key: str = ""
    storage_secret_key: str = ""
    storage_bucket_name: str = ""
    storage_region: str = "eu-central-1"

    model_config = SettingsConfigDict(
        env_prefix="THREEDTREES_",
        case_sensitive=False,
    )


@lru_cache
def get_settings(**kwargs: Any) -> Settings:
    """
    Get settings instance with optional overrides.

    Args:
        **kwargs: Keyword arguments to override settings values.
                 These take precedence over environment variables.

    Returns:
        Settings: Settings instance with applied overrides.
    """
    try:
        if kwargs:
            settings = Settings(**kwargs)
        else:
            settings = Settings()
        return settings
    except Exception as e:
        raise ValueError("Failed to load settings. Ensure all required environment variables " f"with prefix THREEDTREES_ are set. Error: {str(e)}") from e


# For backwards compatibility and default usage
settings = get_settings()
