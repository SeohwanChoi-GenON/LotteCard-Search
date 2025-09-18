from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Optional

from configuration.settings.logging_settings import LoggingSettings
from configuration.settings.outbound.datebase_settings import DatabaseSettings
from configuration.settings.inbound.gateway_settings import GatewaySettings
from configuration.settings.outbound.llm_settings import LLMSettings



class AppSettings(BaseSettings):
    # === Application Info ===
    APP_NAME: str = "LOCA Chat API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "LOCA Integrated Chatbot API"

    # === Application Info ===
    DEBUG: bool = True
    ENVIRONMENT: str = Field("development", description="환경 (development/staging/production)")

    # === Server Configuration ===
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    TIMEOUT_KEEP_ALIVE: int = 30

    # === API Configuration ===
    API_V1_PREFIX: str = "/api/v1/kms-talk"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # === 로깅 설정 (통합) ===
    logging: LoggingSettings = Field(default_factory=lambda: LoggingSettings(
        debug_mode=True,  # 기본값, 실제로는 DEBUG 필드로 오버라이드됨
        level="INFO"
    ))

    # === 하위 설정들 ===
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

    def model_post_init(self, __context) -> None:
        """설정 후처리 - DEBUG와 logging.debug_mode 동기화"""
        # DEBUG 모드에 따라 로깅 설정 자동 조정
        self.logging.debug_mode = self.DEBUG

        # 환경별 자동 조정
        if self.ENVIRONMENT == "production":
            self.logging.level = "WARNING"
            self.logging.console_enabled = False
        elif self.ENVIRONMENT == "development":
            self.logging.level = "DEBUG"

    @property
    def is_development(self) -> bool:
        """개발 환경 여부"""
        return self.DEBUG or self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """운영 환경 여부"""
        return not self.DEBUG and self.ENVIRONMENT == "production"


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
