import tomllib
from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.models import Settings as DocumentSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    api_key: SecretStr


@lru_cache
def get_settings() -> Settings:
    return Settings()


def load_document_settings(config_path: Path) -> DocumentSettings:
    """Load and validate document settings from a TOML file."""

    with config_path.open("rb") as file:
        config_data = tomllib.load(file)

    return DocumentSettings.model_validate(config_data)
