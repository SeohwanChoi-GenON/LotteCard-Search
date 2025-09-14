"""
Configuration Layer 공통 타입 정의
"""

from enum import Enum
from typing import Optional, Dict, Any, Union, List
from pydantic import BaseModel
from datetime import datetime


class DeploymentEnvironment(str, Enum):
    """배포 환경 타입"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    LOCAL = "local"

    @classmethod
    def from_string(cls, env_str: str) -> 'DeploymentEnvironment':
        """문자열에서 DeploymentEnvironment 생성"""
        return cls(env_str.lower())

    def is_production(self) -> bool:
        """운영 환경 여부"""
        return self == self.PRODUCTION

    def is_development(self) -> bool:
        """개발 환경 여부"""
        return self in [self.DEVELOPMENT, self.LOCAL]

    def is_staging(self) -> bool:
        """스테이징 환경 여부"""
        return self == self.STAGING


class LogLevel(str, Enum):
    """로그 레벨"""
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class ServiceStatus(str, Enum):
    """서비스 상태"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    DEGRADED = "degraded"


class ConfigValidationResult(BaseModel):
    """설정 검증 결과"""
    valid: bool
    config_name: str
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()


class ConfigurationError(Exception):
    """설정 관련 예외"""

    def __init__(self, message: str, config_name: str = None, details: Dict[str, Any] = None):
        self.config_name = config_name
        self.details = details or {}
        super().__init__(message)


class MissingConfigurationError(ConfigurationError):
    """필수 설정이 누락된 경우의 예외"""
    pass


class InvalidConfigurationError(ConfigurationError):
    """잘못된 설정 값이 제공된 경우의 예외"""
    pass


# 🎯 타입 별칭들
ConfigDict = Dict[str, Any]
ValidationResults = Dict[str, ConfigValidationResult]
ServiceHealthStatus = Dict[str, ServiceStatus]