"""
환경별 설정 관리
"""
from pydantic import Field
from pydantic_settings import BaseSettings
from ..._types import DeploymentEnvironment


class EnvironmentConfig(BaseSettings):
    """환경별 설정"""

    deployment_env: DeploymentEnvironment

    # 환경별 기능 플래그
    enable_debug_endpoints: bool = Field(False, env="LOCA_ENABLE_DEBUG_ENDPOINTS")
    enable_experimental_features: bool = Field(False, env="LOCA_ENABLE_EXPERIMENTAL")
    enable_swagger_ui: bool = Field(True, env="LOCA_ENABLE_SWAGGER_UI")

    # 환경별 타임아웃 설정
    request_timeout: int = Field(30, env="LOCA_REQUEST_TIMEOUT")
    db_timeout: int = Field(10, env="LOCA_DB_TIMEOUT")

    # 환경별 제한 설정
    max_request_size: int = Field(10485760, env="LOCA_MAX_REQUEST_SIZE")  # 10MB
    rate_limit_per_minute: int = Field(100, env="LOCA_RATE_LIMIT_PER_MINUTE")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 환경별 자동 설정 조정
        self._adjust_for_environment()

    def _adjust_for_environment(self):
        """환경에 따른 설정 자동 조정"""
        if self.deployment_env == DeploymentEnvironment.DEVELOPMENT:
            self.enable_debug_endpoints = True
            self.enable_experimental_features = True
            self.request_timeout = 60  # 개발 환경은 타임아웃 길게

        elif self.deployment_env == DeploymentEnvironment.LOCAL:
            self.enable_debug_endpoints = True
            self.enable_swagger_ui = True
            self.rate_limit_per_minute = 1000  # 로컬은 제한 완화

        elif self.deployment_env == DeploymentEnvironment.PRODUCTION:
            self.enable_debug_endpoints = False
            self.enable_experimental_features = False
            self.enable_swagger_ui = False  # 운영에서는 Swagger UI 비활성화
            self.rate_limit_per_minute = 60  # 운영에서는 제한 강화

    def get_cors_settings(self) -> dict:
        """CORS 설정 반환"""
        if self.deployment_env.is_production():
            return {
                "allow_origins": ["https://loca.lottecard.co.kr"],
                "allow_credentials": True,
                "allow_methods": ["GET", "POST"],
                "allow_headers": ["*"],
            }
        else:
            return {
                "allow_origins": ["*"],
                "allow_credentials": True,
                "allow_methods": ["*"],
                "allow_headers": ["*"],
            }

    class Config:
        env_prefix = "LOCA_ENV_"
        case_sensitive = False