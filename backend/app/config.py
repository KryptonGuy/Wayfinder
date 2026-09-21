from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Config Google Studio
    google_api_key: str | None = Field(default=None, alias="GOOGLE_API_KEY")
    google_model: str | None = Field(default=None, alias="GOOGLE_MODEL")

    #TODO: Open AI Config
    #TODO: Open Router Config

    cors_origins: List[str] = Field(default=["http://localhost:9999"], alias="CORS_ORIGINS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()