"""
데이터베이스 설정
"""
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from ..._types import DeploymentEnvironment
from typing import Optional


class DatabaseConfig(BaseSettings):
    """데이터베이스 설정"""

    deployment_env: DeploymentEnvironment

    # 데이터베이스 연결
    database_url: str = Field(..., env="LOCA_DATABASE_URL")
    database_driver: str = Field("postgresql", env="LOCA_DATABASE_DRIVER")

    # 연결 풀 설정
    max_connections: int = Field(10, env="LOCA_DB_MAX_CONNECTIONS")
    min_connections: int = Field(1, env="LOCA_DB_MIN_CONNECTIONS")
    connection_timeout: int = Field(30, env="LOCA_DB_CONNECTION_TIMEOUT")

    # 쿼리 설정
    query_timeout: int = Field(30, env="LOCA_DB_QUERY_TIMEOUT")
    statement_timeout: int = Field(60, env="LOCA_DB_STATEMENT_TIMEOUT")

    # 기타 설정
    echo_sql: bool = Field(False, env="LOCA_DB_ECHO_SQL")
    auto_commit: bool = Field(False, env="LOCA_DB_AUTO_COMMIT")

    @validator('max_connections')
    def validate_max_connections(cls, v, values):
        min_conn = values.get('min_connections', 1)
        if v < min_conn:
            raise ValueError(f'max_connections ({v}) must be >= min_connections ({min_conn})')
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 환경별 설정 조정
        if self.deployment_env == DeploymentEnvironment.DEVELOPMENT:
            self.echo_sql = True
            self.max_connections = 5
        elif self.deployment_env == DeploymentEnvironment.PRODUCTION:
            self.max_connections = 20
            self.echo_sql = False

    def get_sqlalchemy_config(self) -> dict:
        """SQLAlchemy 엔진 설정 반환"""
        return {
            "url": self.database_url,
            "echo": self.echo_sql,
            "pool_size": self.max_connections,
            "max_overflow": self.max_connections * 2,
            "pool_timeout": self.connection_timeout,
            "pool_recycle": 3600,
            "pool_pre_ping": True
        }

    class Config:
        env_prefix = "LOCA_DB_"
        case_sensitive = False