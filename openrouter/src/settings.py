# settings.py
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """OpenRouter 설정 - Pydantic v2 기반"""

    # **필수 설정**
    openrouter_api_key: str = Field(..., description="OpenRouter API 키")

    # **기본 설정**
    max_tokens: int = Field(1000, ge=1, le=8192, description="최대 토큰 수")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="창의성 온도")
    timeout: float = Field(30.0, ge=1.0, description="타임아웃(초)")

    # **선호 모델**
    preferred_models: List[str] = Field(
        default=[
            "claude-4-sonnet",
            "gpt-4.1-mini",
            "qwen3-next-80b",
            "gpt-oss"
        ],
        description="선호 모델 목록"
    )

    @field_validator('openrouter_api_key')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v.startswith('sk-or-v1-'):
            raise ValueError('OpenRouter API 키는 sk-or-v1-로 시작해야 합니다')
        return v

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


def get_settings() -> Settings:
    """설정 인스턴스 반환"""
    return Settings()