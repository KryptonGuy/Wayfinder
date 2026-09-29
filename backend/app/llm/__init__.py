from collections.abc import Callable

from langchain_core.language_models import BaseChatModel

from app.config import get_settings
from app.llm import google, openrouter

# Register new providers here; the key is the value accepted by LLM_PROVIDER.
PROVIDERS: dict[str, Callable[..., BaseChatModel]] = {
    "google": google.build,
    "openrouter": openrouter.build,
}


def get_llm(provider: str | None = None, model: str | None = None, **kwargs) -> BaseChatModel:
    """Build a chat model; provider/model default to the configured values."""
    settings = get_settings()
    provider = provider or settings.llm_provider
    try:
        builder = PROVIDERS[provider]
    except KeyError:
        raise ValueError(
            f"Unknown LLM provider '{provider}'. Available: {', '.join(PROVIDERS)}"
        ) from None
    return builder(settings, model, **kwargs)


__all__ = ["get_llm"]
