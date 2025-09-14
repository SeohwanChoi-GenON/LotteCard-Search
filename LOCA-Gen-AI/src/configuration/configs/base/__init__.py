"""
Base Configuration Domain : 시스템의 기본적인 설정들을 관리하는 도메인

포함되는 설정:
- AppConfig: 애플리케이션 기본 설정 (API, 문서화 등)
- EnvironmentConfig: 환경별 설정 관리
"""

from .app_config import AppConfig
from .environment_config import EnvironmentConfig

# Base Domain Public API
__all__ = [
    "AppConfig",
    "EnvironmentConfig",
]


def get_base_config_info() -> dict:
    """Base 설정 도메인 정보"""
    return {
        "domain": "base",
        "description": "기본 시스템 설정",
        "configs": {
            "AppConfig": {
                "description": "애플리케이션 기본 설정",
                "responsibilities": [
                    "API 서버 설정",
                    "문서화 설정",
                    "기본 앱 메타데이터",
                    "Uvicorn 서버 설정"
                ]
            },
            "EnvironmentConfig": {
                "description": "환경별 설정 관리",
                "responsibilities": [
                    "환경별 기본값 설정",
                    "환경 감지 및 분기",
                    "환경별 기능 활성화/비활성화",
                    "CORS 설정 관리"
                ]
            }
        }
    }


def validate_base_configs(deployment_env) -> dict:
    """Base 도메인 설정들 유효성 검사"""
    results = {}

    try:
        # AppConfig 검증
        app_config = AppConfig(
            deployment_env=deployment_env,
            debug_mode=deployment_env.value in ["development", "local"]
        )
        results["AppConfig"] = {
            "valid": True,
            "instance": "created_successfully",
            "uvicorn_config": app_config.get_uvicorn_config()
        }

    except Exception as e:
        results["AppConfig"] = {
            "valid": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

    try:
        # EnvironmentConfig 검증
        env_config = EnvironmentConfig(deployment_env=deployment_env)
        results["EnvironmentConfig"] = {
            "valid": True,
            "instance": "created_successfully",
            "cors_settings": env_config.get_cors_settings()
        }

    except Exception as e:
        results["EnvironmentConfig"] = {
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


def create_base_configs(deployment_env, debug_mode: bool = False):
    """Base 도메인 설정들 생성 팩토리"""
    return {
        "app": AppConfig(
            deployment_env=deployment_env,
            debug_mode=debug_mode
        ),
        "environment": EnvironmentConfig(
            deployment_env=deployment_env
        )
    }