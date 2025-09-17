"""LLM 설정"""

from pydantic import Field
from pydantic_settings import BaseSettings


class LLMSettings(BaseSettings):
    provider: str = Field(default="openai", env="LLM_PROVIDER")  # ✅ 이제 env 사용 가능
    api_key: str = Field(default="", env="LLM_API_KEY")
    model: str = Field(default="gpt-4", env="LLM_MODEL")
    max_tokens: int = Field(default=2000, env="LLM_MAX_TOKENS")
    temperature: float = Field(default=0.1, env="LLM_TEMPERATURE")

    class Config:
        env_file = ".env"
        extra = "ignore"
