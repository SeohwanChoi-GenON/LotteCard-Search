# src/infrastructure/config/constants.py

class UvicornConfig:
    """Uvicorn 서버 설정 상수"""
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    LOG_LEVEL: str = "info"
    TIMEOUT_KEEP_ALIVE: int = 5

class APIConstants:
    """API 관련 상수"""
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    REQUEST_TIMEOUT: int = 30

class CacheConstants:
    """캐시 관련 상수"""
    DEFAULT_TTL: int = 300  # 5분
    SESSION_TTL: int = 1800  # 30분
    TEMPLATE_CACHE_TTL: int = 3600  # 1시간
