"""
LangChain 설정
"""
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from ..._types import DeploymentEnvironment
from typing import Optional, Dict, Any


class LangChainConfig(BaseSettings):
    """LangChain 관련 설정"""

    deployment_env: DeploymentEnvironment
    debug_mode: bool = False

    # LangSmith 설정 (추적 및 디버깅)
    langsmith_api_key: str = Field(..., env="LANGSMITH_API_KEY")
    langsmith_project: str = Field("loca-gen-ai", env="LANGSMITH_PROJECT")
    langsmith_endpoint: str = Field("https://api.smith.langchain.com", env="LANGSMITH_ENDPOINT")
    langsmith_tracing_enabled: bool = Field(True, env="LANGSMITH_TRACING_ENABLED")

    # LangChain 실행 설정
    langchain_cache_enabled: bool = Field(True, env="LANGCHAIN_CACHE_ENABLED")
    langchain_verbose: bool = Field(False, env="LANGCHAIN_VERBOSE")
    langchain_debug: bool = Field(False, env="LANGCHAIN_DEBUG")

    # 메모리 및 성능 설정
    max_memory_tokens: int = Field(4000, env="LANGCHAIN_MAX_MEMORY_TOKENS")
    max_iterations: int = Field(15, env="LANGCHAIN_MAX_ITERATIONS")
    request_timeout: int = Field(60, env="LANGCHAIN_REQUEST_TIMEOUT")

    # 체인 설정
    temperature: float = Field(0.7, env="LANGCHAIN_TEMPERATURE")
    max_tokens: int = Field(1000, env="LANGCHAIN_MAX_TOKENS")

    # 벡터 스토어 설정
    embedding_chunk_size: int = Field(1000, env="LANGCHAIN_EMBEDDING_CHUNK_SIZE")
    embedding_chunk_overlap: int = Field(200, env="LANGCHAIN_EMBEDDING_CHUNK_OVERLAP")

    @validator('temperature')
    def validate_temperature(cls, v):
        if not (0.0 <= v <= 2.0):
            raise ValueError('Temperature must be between 0.0 and 2.0')
        return v

    @validator('max_iterations')
    def validate_max_iterations(cls, v):
        if v < 1:
            raise ValueError('Max iterations must be at least 1')
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 환경별 설정 조정
        self._adjust_for_environment()

    def _adjust_for_environment(self):
        """환경별 LangChain 설정 조정"""
        if self.deployment_env == DeploymentEnvironment.DEVELOPMENT:
            self.langchain_verbose = self.debug_mode
            self.langchain_debug = True
            self.langsmith_tracing_enabled = True
            self.request_timeout = 120  # 개발에서는 타임아웃 길게

        elif self.deployment_env == DeploymentEnvironment.LOCAL:
            self.langchain_verbose = True
            self.langsmith_tracing_enabled = True
            self.temperature = 0.1  # 로컬에서는 일관된 결과를 위해

        elif self.deployment_env == DeploymentEnvironment.PRODUCTION:
            self.langchain_verbose = False
            self.langchain_debug = False
            self.langsmith_tracing_enabled = False  # 운영에서는 추적 비활성화
            self.max_iterations = 10  # 운영에서는 반복 제한

    def get_langsmith_config(self) -> Dict[str, Any]:
        """LangSmith 설정 딕셔너리 반환"""
        return {
            "api_key": self.langsmith_api_key,
            "project": self.langsmith_project,
            "endpoint": self.langsmith_endpoint,
            "tracing_enabled": self.langsmith_tracing_enabled
        }

    def get_chain_config(self) -> Dict[str, Any]:
        """체인 기본 설정 딕셔너리 반환"""
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "max_iterations": self.max_iterations,
            "verbose": self.langchain_verbose,
            "request_timeout": self.request_timeout
        }

    def get_text_splitter_config(self) -> Dict[str, Any]:
        """텍스트 분할 설정 반환"""
        return {
            "chunk_size": self.embedding_chunk_size,
            "chunk_overlap": self.embedding_chunk_overlap,
            "length_function": len,
            "separators": ["\n\n", "\n", " ", ""]
        }

    class Config:
        env_prefix = "LOCA_LANGCHAIN_"
        case_sensitive = False