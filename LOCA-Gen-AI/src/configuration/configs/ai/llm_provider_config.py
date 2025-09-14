"""
LLM Provider 설정
"""
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from ..._types import DeploymentEnvironment
from typing import Optional, Dict, Any, List
from enum import Enum


class LLMProvider(str, Enum):
    """지원하는 LLM 제공자"""
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"


class OpenAIModel(str, Enum):
    """OpenAI 모델들"""
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4O = "gpt-4o"
    GPT_35_TURBO = "gpt-3.5-turbo"


class LLMProviderConfig(BaseSettings):
    """LLM Provider 설정"""

    deployment_env: DeploymentEnvironment

    # 기본 Provider 설정
    default_provider: LLMProvider = Field(LLMProvider.OPENAI, env="LOCA_LLM_DEFAULT_PROVIDER")
    fallback_provider: Optional[LLMProvider] = Field(None, env="LOCA_LLM_FALLBACK_PROVIDER")

    # OpenAI 설정
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_organization: Optional[str] = Field(None, env="OPENAI_ORGANIZATION")
    openai_base_url: str = Field("https://api.openai.com/v1", env="OPENAI_BASE_URL")
    openai_default_model: OpenAIModel = Field(OpenAIModel.GPT_4O, env="LOCA_OPENAI_DEFAULT_MODEL")

    # Azure OpenAI 설정 (선택적)
    azure_openai_api_key: Optional[str] = Field(None, env="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: Optional[str] = Field(None, env="AZURE_OPENAI_ENDPOINT")
    azure_openai_version: str = Field("2024-02-01", env="AZURE_OPENAI_VERSION")

    # LLM 실행 파라미터
    default_temperature: float = Field(0.7, env="LOCA_LLM_TEMPERATURE")
    default_max_tokens: int = Field(4000, env="LOCA_LLM_MAX_TOKENS")
    default_top_p: float = Field(1.0, env="LOCA_LLM_TOP_P")
    default_frequency_penalty: float = Field(0.0, env="LOCA_LLM_FREQUENCY_PENALTY")
    default_presence_penalty: float = Field(0.0, env="LOCA_LLM_PRESENCE_PENALTY")

    # 요청 설정
    request_timeout: int = Field(60, env="LOCA_LLM_REQUEST_TIMEOUT")
    max_retries: int = Field(3, env="LOCA_LLM_MAX_RETRIES")
    retry_delay: float = Field(1.0, env="LOCA_LLM_RETRY_DELAY")

    # 토큰 관리
    max_context_tokens: int = Field(128000, env="LOCA_LLM_MAX_CONTEXT_TOKENS")  # GPT-4 기준
    reserved_tokens_for_response: int = Field(4000, env="LOCA_LLM_RESERVED_TOKENS")

    # 스트리밍 설정
    enable_streaming: bool = Field(True, env="LOCA_LLM_ENABLE_STREAMING")
    stream_chunk_size: int = Field(1024, env="LOCA_LLM_STREAM_CHUNK_SIZE")

    @validator('default_temperature', 'default_top_p')
    def validate_probability_params(cls, v):
        if not (0.0 <= v <= 2.0):
            raise ValueError('Parameter must be between 0.0 and 2.0')
        return v

    @validator('default_frequency_penalty', 'default_presence_penalty')
    def validate_penalty_params(cls, v):
        if not (-2.0 <= v <= 2.0):
            raise ValueError('Penalty must be between -2.0 and 2.0')
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 환경별 설정 조정
        self._adjust_for_environment()

    def _adjust_for_environment(self):
        """환경별 LLM 설정 조정"""
        if self.deployment_env == DeploymentEnvironment.DEVELOPMENT:
            self.openai_default_model = OpenAIModel.GPT_35_TURBO  # 개발에서는 더 저렴한 모델
            self.request_timeout = 120
            self.max_retries = 5

        elif self.deployment_env == DeploymentEnvironment.LOCAL:
            self.openai_default_model = OpenAIModel.GPT_35_TURBO
            self.default_temperature = 0.1  # 로컬에서는 일관된 결과
            self.enable_streaming = False  # 로컬에서는 스트리밍 비활성화

        elif self.deployment_env == DeploymentEnvironment.PRODUCTION:
            self.openai_default_model = OpenAIModel.GPT_4O  # 운영에서는 최신 모델
            self.max_retries = 2  # 운영에서는 빠른 실패
            self.request_timeout = 30

    def get_openai_client_config(self) -> Dict[str, Any]:
        """OpenAI 클라이언트 설정 반환"""
        config = {
            "api_key": self.openai_api_key,
            "base_url": self.openai_base_url,
            "timeout": self.request_timeout,
            "max_retries": self.max_retries,
        }

        if self.openai_organization:
            config["organization"] = self.openai_organization

        return config

    def get_default_completion_params(self) -> Dict[str, Any]:
        """기본 completion 파라미터 반환"""
        return {
            "model": self.openai_default_model.value,
            "temperature": self.default_temperature,
            "max_tokens": self.default_max_tokens,
            "top_p": self.default_top_p,
            "frequency_penalty": self.default_frequency_penalty,
            "presence_penalty": self.default_presence_penalty,
            "stream": self.enable_streaming,
        }

    def get_available_context_tokens(self) -> int:
        """응답을 위해 예약된 토큰을 제외한 사용 가능한 컨텍스트 토큰 수"""
        return self.max_context_tokens - self.reserved_tokens_for_response

    def should_use_fallback(self, error_type: str) -> bool:
        """오류 타입에 따른 폴백 사용 여부 결정"""
        fallback_triggers = [
            "rate_limit_error",
            "service_unavailable",
            "timeout_error",
            "api_error"
        ]
        return self.fallback_provider is not None and error_type in fallback_triggers

    class Config:
        env_prefix = "LOCA_LLM_"
        case_sensitive = False
        use_enum_values = True