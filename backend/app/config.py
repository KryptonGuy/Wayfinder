from functools import lru_cache
from typing import List, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM provider, either google or openrouter
    llm_provider: Literal["google", "openrouter"] = Field(
        default="google", alias="LLM_PROVIDER"
    )

    # Config Google APIS
    google_api_key: str | None = Field(default=None, alias="GOOGLE_API_KEY")
    google_model: str | None = Field(default=None, alias="GOOGLE_MODEL")

    # Config Open Router APIs
    openrouter_api_key: str | None = Field(default=None, alias="OPENROUTER_API_KEY")
    openrouter_model: str = Field(
        default="google/gemma-4-31b-it:free", alias="OPENROUTER_MODEL"
    )

    #TODO: Add Open AI APIs

    cors_origins: List[str] = Field(default=["http://localhost:9999"], alias="CORS_ORIGINS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()