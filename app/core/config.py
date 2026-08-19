from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App ---
    app_env: str = "development"
    log_level: str = "INFO"

    # --- Database ---
    database_url: str

    # --- LLM Providers ---
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None
    groq_api_key: str | None = None
    gemini_api_key: str | None = None
    mistral_api_key: str | None = None

    # --- Model routing (format: "<provider>:<model>") ---
    supervisor_model: str = "gemini:gemini-2.5-flash"
    worker_model: str = "groq:llama-3.1-8b-instant"

    # --- Observability ---
    langsmith_api_key: str | None = None
    langsmith_project: str = "ops-pilot"
    langsmith_tracing: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()