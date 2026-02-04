"""Application settings loaded from environment variables and .env file."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    # Groq / LLM
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_model: str = "llama-3.3-70b-versatile"

    # E-REDES API
    eredes_api_base: str = "https://e-redes.opendatasoft.com/api/v2/catalog/datasets"
    eredes_dataset: str = "network-scheduling-work"

    # Chat
    max_messages: int = 50
    chat_timeout_seconds: int = 60

    # Rate limiting
    rate_limit: str = "10/minute"

    # CORS
    allowed_origins: str = "*"

    # Logging
    log_level: str = "INFO"


settings = Settings()

# Keep EMERGENCY_CONTACTS as a plain dict (not configurable)
EMERGENCY_CONTACTS = {
    "linha_avarias": "800 506 506",
    "emergencia": "112",
    "balcao_digital": "https://balcaodigital.e-redes.pt",
    "protecao_civil": "214 247 100",
}
