from pydantic_settings import BaseSettings
from typing import List


class AppSettings(BaseSettings):
    # Application
    APP_NAME: str = "LOCA Chat API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "LOCA Integrated Chatbot API"
    DEBUG: bool = True

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    LOG_LEVEL: str = "info"
    TIMEOUT_KEEP_ALIVE: int = 30

    # API
    API_V1_PREFIX: str = "/api/v1/kms-talk"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Elasticsearch
    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_USERNAME: str = ""
    ELASTICSEARCH_PASSWORD: str = ""

    # LLM
    LLM_API_BASE: str = ""
    LLM_MODEL_NAME: str = ""
    LLM_API_KEY: str = "EMPTY"

    class Config:
        env_file = ".env"


_settings = None

def get_settings() -> AppSettings:
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings