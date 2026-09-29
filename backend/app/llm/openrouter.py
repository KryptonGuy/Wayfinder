from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from app.config import Settings

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def build(settings: Settings, model: str | None, **kwargs) -> BaseChatModel:
    if not settings.openrouter_api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not configured")
    return ChatOpenAI(
        api_key=settings.openrouter_api_key,
        base_url=OPENROUTER_BASE_URL,
        model=model or settings.openrouter_model,
        **kwargs,
    )
