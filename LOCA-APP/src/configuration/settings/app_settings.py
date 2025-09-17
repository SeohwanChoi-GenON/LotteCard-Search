from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Optional

from configuration.settings.datebase_settings import DatabaseSettings
from configuration.settings.gateway_settings import GatewaySettings
from configuration.settings.llm_settings import LLMSettings



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

    # === 하위 설정들 ===rmrp
    gateway: GatewaySettings = Field(default_factory=GatewaySettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)

    # # Elasticsearch
    # ELASTICSEARCH_HOST: str = "localhost"
    # ELASTICSEARCH_PORT: int = 9200
    # ELASTICSEARCH_USERNAME: str = ""
    # ELASTICSEARCH_PASSWORD: str = ""
    #
    # # LLM
    # LLM_API_BASE: str = ""
    # LLM_MODEL_NAME: str = ""
    # LLM_API_KEY: str = "EMPTY"

    class Config:
        env_file = str(Path(__file__).parent.parent.parent / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True
        env_nested_delimiter = '__'  # GATEWAY__ENABLED 형태 지원
        extra = "ignore"


# === 전역 싱글톤 인스턴스 ===
_settings: Optional[AppSettings] = None


def get_settings() -> AppSettings:
    """설정 인스턴스 반환 (싱글톤 패턴)"""
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings

def reload_settings() -> AppSettings:
    """설정 재로드 (테스트나 런타임 설정 변경 시 사용)"""
    global _settings
    _settings = None
    return get_settings()
