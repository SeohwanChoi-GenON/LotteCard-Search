"""
Redis 설정
"""
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from ..._types import DeploymentEnvironment
from typing import Optional


class RedisConfig(BaseSettings):
    """Redis 설정"""

    deployment_env: DeploymentEnvironment

    # Redis 연결
    redis_url: str = Field("redis://localhost:6379/0", env="LOCA_REDIS_URL")
    redis_host: str = Field("localhost", env="LOCA_REDIS_HOST")
    redis_port: int = Field(6379, env="LOCA_REDIS_PORT")
    redis_db: int = Field(0, env="LOCA_REDIS_DB")
    redis_password: Optional[str] = Field(None, env="LOCA_REDIS_PASSWORD")

    # 연결 풀 설정
    max_connections: int = Field(10, env="LOCA_REDIS_MAX_CONNECTIONS")
    connection_timeout: int = Field(5, env="LOCA_REDIS_CONNECTION_TIMEOUT")
    socket_timeout: int = Field(5, env="LOCA_REDIS_SOCKET_TIMEOUT")

    # 캐시 설정
    default_ttl: int = Field(3600, env="LOCA_REDIS_DEFAULT_TTL")  # 1시간
    session_ttl: int = Field(86400, env="LOCA_REDIS_SESSION_TTL")  # 24시간

    # 키 프리픽스
    key_prefix: str = Field("loca:", env="LOCA_REDIS_KEY_PREFIX")
    session_prefix: str = Field("session:", env="LOCA_REDIS_SESSION_PREFIX")
    cache_prefix: str = Field("cache:", env="LOCA_REDIS_CACHE_PREFIX")

    @validator('redis_port')
    def validate_port(cls, v):
        if not (1 <= v <= 65535):
            raise ValueError('Redis port must be between 1 and 65535')
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 환경별 설정 조정
        if self.deployment_env == DeploymentEnvironment.PRODUCTION:
            self.max_connections = 50
            self.default_ttl = 7200  # 운영에서는 캐시를 더 오래
        elif self.deployment_env.is_development():
            self.default_ttl = 600  # 개발에서는 짧게

    def get_redis_connection_config(self) -> dict:
        """Redis 연결 설정 반환"""
        config = {
            "host": self.redis_host,
            "port": self.redis_port,
            "db": self.redis_db,
            "socket_timeout": self.socket_timeout,
            "socket_connect_timeout": self.connection_timeout,
            "decode_responses": True,
            "max_connections": self.max_connections,
        }

        if self.redis_password:
            config["password"] = self.redis_password

        return config

    def get_cache_key(self, key: str, category: str = "cache") -> str:
        """캐시 키 생성"""
        prefix_map = {
            "cache": self.cache_prefix,
            "session": self.session_prefix
        }
        prefix = prefix_map.get(category, self.cache_prefix)
        return f"{self.key_prefix}{prefix}{key}"

    class Config:
        env_prefix = "LOCA_REDIS_"
        case_sensitive = False