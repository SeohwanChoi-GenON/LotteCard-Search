"""
모니터링 설정
"""
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from ..._types import DeploymentEnvironment, LogLevel
from typing import Optional, List


class MonitoringConfig(BaseSettings):
    """모니터링 설정"""

    deployment_env: DeploymentEnvironment
    enable_tracing: bool = True

    # 로깅 설정
    log_level: LogLevel = Field(LogLevel.INFO, env="LOCA_LOG_LEVEL")
    log_format: str = Field("%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOCA_LOG_FORMAT")
    log_file_path: Optional[str] = Field(None, env="LOCA_LOG_FILE_PATH")
    max_log_file_size: int = Field(10485760, env="LOCA_MAX_LOG_FILE_SIZE")  # 10MB
    log_backup_count: int = Field(5, env="LOCA_LOG_BACKUP_COUNT")

    # 메트릭 설정
    metrics_enabled: bool = Field(True, env="LOCA_METRICS_ENABLED")
    metrics_port: int = Field(8090, env="LOCA_METRICS_PORT")
    metrics_path: str = Field("/metrics", env="LOCA_METRICS_PATH")

    # 헬스체크 설정
    health_check_enabled: bool = Field(True, env="LOCA_HEALTH_CHECK_ENABLED")
    health_check_path: str = Field("/health", env="LOCA_HEALTH_CHECK_PATH")
    health_check_interval: int = Field(30, env="LOCA_HEALTH_CHECK_INTERVAL")

    # 알림 설정
    alerting_enabled: bool = Field(False, env="LOCA_ALERTING_ENABLED")
    alert_webhook_url: Optional[str] = Field(None, env="LOCA_ALERT_WEBHOOK_URL")
    alert_channels: List[str] = Field(default_factory=list, env="LOCA_ALERT_CHANNELS")

    # 추적 설정
    tracing_sample_rate: float = Field(0.1, env="LOCA_TRACING_SAMPLE_RATE")
    tracing_service_name: str = Field("loca-gen-ai", env="LOCA_TRACING_SERVICE_NAME")

    @validator('tracing_sample_rate')
    def validate_sample_rate(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError('Tracing sample rate must be between 0.0 and 1.0')
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 환경별 설정 조정
        self._adjust_for_environment()

    def _adjust_for_environment(self):
        """환경별 모니터링 설정 조정"""
        if self.deployment_env == DeploymentEnvironment.DEVELOPMENT:
            self.log_level = LogLevel.DEBUG
            self.tracing_sample_rate = 1.0  # 개발에서는 모든 요청 추적
            self.metrics_enabled = True

        elif self.deployment_env == DeploymentEnvironment.LOCAL:
            self.log_level = LogLevel.DEBUG
            self.tracing_sample_rate = 1.0
            self.health_check_enabled = False  # 로컬에서는 헬스체크 불필요

        elif self.deployment_env == DeploymentEnvironment.PRODUCTION:
            self.log_level = LogLevel.WARNING
            self.tracing_sample_rate = 0.01  # 운영에서는 1%만 추적
            self.alerting_enabled = True
            self.log_file_path = "/var/log/loca/app.log"

    def get_logging_config(self) -> dict:
        """로깅 설정 딕셔너리 반환"""
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": self.log_format
                },
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": self.log_level.value,
                    "formatter": "standard",
                    "stream": "ext://sys.stdout"
                }
            },
            "loggers": {
                "": {
                    "handlers": ["console"],
                    "level": self.log_level.value,
                    "propagate": False
                }
            }
        }

        # 파일 핸들러 추가 (설정된 경우)
        if self.log_file_path:
            config["handlers"]["file"] = {
                "class": "logging.handlers.RotatingFileHandler",
                "level": self.log_level.value,
                "formatter": "detailed",
                "filename": self.log_file_path,
                "maxBytes": self.max_log_file_size,
                "backupCount": self.log_backup_count
            }
            config["loggers"][""]["handlers"].append("file")

        return config

    def should_trace_request(self) -> bool:
        """요청 추적 여부 결정"""
        import random
        return random.random() < self.tracing_sample_rate

    class Config:
        env_prefix = "LOCA_MONITORING_"
        case_sensitive = False