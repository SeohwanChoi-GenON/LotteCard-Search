"""
🔧 Infrastructure Configuration Domain : 시스템의 인프라스트럭처 관련 설정들을 관리하는 도메인

포함되는 설정:
- DatabaseConfig: 데이터베이스 연결 및 설정
- RedisConfig: Redis 캐시 및 세션 설정
- MonitoringConfig: 모니터링, 로깅, 추적 설정
"""

from .database_config import DatabaseConfig
from .redis_config import RedisConfig
from .monitoring_config import MonitoringConfig

# Infrastructure Domain Public API
__all__ = [
    "DatabaseConfig",
    "RedisConfig",
    "MonitoringConfig",
]


def get_infrastructure_config_info() -> dict:
    """Infrastructure 설정 도메인 정보"""
    return {
        "domain": "infrastructure",
        "description": "인프라스트럭처 관련 설정",
        "configs": {
            "DatabaseConfig": {
                "description": "데이터베이스 연결 설정",
                "responsibilities": [
                    "DB 연결 문자열 관리",
                    "커넥션 풀 설정",
                    "환경별 DB 설정",
                    "SQLAlchemy 엔진 설정"
                ]
            },
            "RedisConfig": {
                "description": "Redis 캐시 설정",
                "responsibilities": [
                    "Redis 연결 설정",
                    "캐시 정책 관리",
                    "세션 스토어 설정",
                    "키 네이밍 규칙"
                ]
            },
            "MonitoringConfig": {
                "description": "모니터링 설정",
                "responsibilities": [
                    "로깅 설정",
                    "메트릭 수집 설정",
                    "추적 및 알림 설정",
                    "헬스체크 설정"
                ]
            }
        }
    }


def validate_infrastructure_configs(deployment_env) -> dict:
    """Infrastructure 도메인 설정들 유효성 검사"""
    results = {}

    # DatabaseConfig 검증
    try:
        db_config = DatabaseConfig(deployment_env=deployment_env)
        results["DatabaseConfig"] = {
            "valid": True,
            "connection_test": "pending",
            "sqlalchemy_config": db_config.get_sqlalchemy_config()
        }
    except Exception as e:
        results["DatabaseConfig"] = {
            "valid": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

    # RedisConfig 검증
    try:
        redis_config = RedisConfig(deployment_env=deployment_env)
        results["RedisConfig"] = {
            "valid": True,
            "connection_test": "pending",
            "connection_config": redis_config.get_redis_connection_config()
        }
    except Exception as e:
        results["RedisConfig"] = {
            "valid": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

    # MonitoringConfig 검증
    try:
        monitoring_config = MonitoringConfig(
            deployment_env=deployment_env,
            enable_tracing=True
        )
        results["MonitoringConfig"] = {
            "valid": True,
            "tracing_enabled": monitoring_config.enable_tracing,
            "logging_config": monitoring_config.get_logging_config()
        }
    except Exception as e:
        results["MonitoringConfig"] = {
            "valid": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

    # 전체 유효성
    results["valid"] = all(
        config.get("valid", False)
        for config in results.values()
        if isinstance(config, dict) and "valid" in config
    )

    return results


def create_infrastructure_configs(deployment_env, **kwargs):
    """Infrastructure 도메인 설정들 생성 팩토리"""
    return {
        "database": DatabaseConfig(deployment_env=deployment_env),
        "redis": RedisConfig(deployment_env=deployment_env),
        "monitoring": MonitoringConfig(
            deployment_env=deployment_env,
            enable_tracing=kwargs.get("enable_tracing", True)
        )
    }


async def check_infrastructure_health() -> dict:
    """
    인프라 헬스체크 (실제 연결 테스트)
    주의: 실제 외부 서비스에 연결을 시도합니다.
    """
    health_results = {
        "overall_healthy": False,
        "checks": {}
    }

    # Database 헬스체크 (구현 예정)
    health_results["checks"]["database"] = {
        "status": "unknown",
        "message": "Health check not implemented",
        "response_time_ms": None
    }

    # Redis 헬스체크 (구현 예정)
    health_results["checks"]["redis"] = {
        "status": "unknown",
        "message": "Health check not implemented",
        "response_time_ms": None
    }

    # 전체 상태 결정
    healthy_checks = [
        check["status"] == "healthy"
        for check in health_results["checks"].values()
    ]
    health_results["overall_healthy"] = all(healthy_checks) if healthy_checks else False

    return health_results