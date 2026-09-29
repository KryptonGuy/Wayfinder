from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import Settings


def build(settings: Settings, model: str | None, **kwargs) -> BaseChatModel:
    if not settings.google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured")
    return ChatGoogleGenerativeAI(
        google_api_key=settings.google_api_key,
        model=model or settings.google_model,
        **kwargs,
    )
