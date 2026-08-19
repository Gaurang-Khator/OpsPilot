from app.core.config import get_settings

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel


def get_llm(role: str = "worker") -> BaseChatModel:
    """
        role: 'supervisor' or 'worker' -- picks which model to use from .env
    """

    settings = get_settings()
    model_string = settings.supervisor_model if role == "supervisor" else settings.worker_model

    provider, model_name = model_string.split(":", 1)
    
    # Map provider to API key from settings
    api_key_map = {
        "groq": settings.groq_api_key,
        "openai": settings.openai_api_key,
        "anthropic": settings.anthropic_api_key,
        "google_genai": settings.gemini_api_key,
        "mistral": settings.mistral_api_key,
    }
    
    api_key = api_key_map.get(provider)
    return init_chat_model(model=model_name, model_provider=provider, api_key=api_key)