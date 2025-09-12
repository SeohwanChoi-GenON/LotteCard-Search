# src/infrastructure/config/settings.py
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # 애플리케이션 설정
    APP_NAME: str = Field("Digi LOCA APP ChatBot Service", env="APP_NAME")
    APP_VERSION: str = Field("1.0.0", env="APP_VERSION")
    APP_DESCRIPTION: str = "Digi LOCA ChatBot Service"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redocs"
    DEBUG: bool = Field(False, env="DEBUG")

    # API 설정
    API_V1_PREFIX: str = Field("/api/v1", env="API_V1_PREFIX")
    ALLOWED_ORIGINS: List[str] = Field(["*"], env="ALLOWED_ORIGINS")

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()