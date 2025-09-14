"""
기본 애플리케이션 설정
"""
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from ..._types import DeploymentEnvironment


class AppConfig(BaseSettings):
    """애플리케이션 기본 설정"""

    # API 서버 설정
    api_host: str = Field("0.0.0.0", env="LOCA_API_HOST")
    api_port: int = Field(8000, env="LOCA_API_PORT")
    api_prefix: str = Field("/api/v1", env="LOCA_API_PREFIX")
    api_title: str = Field("LOCA Gen AI API", env="LOCA_API_TITLE")
    api_description: str = Field("LOCA Generative AI ChatBot API", env="LOCA_API_DESCRIPTION")
    api_version: str = Field("2.0.0", env="LOCA_API_VERSION")

    # 문서화 설정
    docs_url: str = Field("/docs", env="LOCA_DOCS_URL")
    redoc_url: str = Field("/redoc", env="LOCA_REDOC_URL")
    openapi_url: str = Field("/openapi.json", env="LOCA_OPENAPI_URL")

    # 서버 설정
    workers: int = Field(1, env="LOCA_WORKERS")
    timeout_keep_alive: int = Field(5, env="LOCA_TIMEOUT_KEEP_ALIVE")

    # 환경 정보 (부모에서 전달)
    deployment_env: DeploymentEnvironment
    debug_mode: bool = False

    @validator('api_port')
    def validate_port(cls, v):
        if not (1024 <= v <= 65535):
            raise ValueError('Port must be between 1024 and 65535')
        return v

    @validator('workers')
    def validate_workers(cls, v):
        if v < 1:
            raise ValueError('Workers must be at least 1')
        return v

    def get_uvicorn_config(self) -> dict:
        """Uvicorn 서버 설정 반환"""
        return {
            "host": self.api_host,
            "port": self.api_port,
            "workers": self.workers,
            "timeout_keep_alive": self.timeout_keep_alive,
            "reload": self.debug_mode
        }

    class Config:
        env_prefix = "LOCA_APP_"
        case_sensitive = False