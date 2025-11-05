"""Application configuration using Pydantic settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application settings
    app_name: str = "Poker API"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # Firebase settings
    firebase_credentials_path: str | None = None
    firebase_project_id: str | None = None

    # CORS settings
    cors_origins: list[str] = ["*"]


settings = Settings()
