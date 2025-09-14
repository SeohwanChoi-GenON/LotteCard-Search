"""
🏆 LOCA Configuration Layer

LOCA 시스템의 모든 설정을 통합 관리하는 Configuration Layer입니다.

주요 구성 요소:
- LOCAConfig: 모든 설정의 마스터 관리자
- LOCAContainer: 의존성 주입 컨테이너
- configs/: 도메인별 하위 설정들

Architecture:
    LOCAConfig (마스터)
    ├── Base Configs (기본 설정)
    │   ├── AppConfig
    │   └── EnvironmentConfig
    ├── Infrastructure Configs (인프라 설정)
    │   ├── DatabaseConfig
    │   ├── RedisConfig
    │   └── MonitoringConfig
    └── AI Configs (AI 설정)
        ├── LangChainConfig
        ├── LLMProviderConfig
        └── ElasticsearchConfig

사용법:
    # 기본 사용
    from configuration import get_loca_config, get_container

    config = get_loca_config()
    container = get_container()

    # 특정 설정 접근
    app_config = config.app
    db_config = config.database
    llm_config = config.llm_provider

    # 시스템 정보 및 검증
    from configuration import get_config_summary, validate_configuration

    summary = get_config_summary()
    is_valid, results = validate_configuration()
"""

# 🏆 Master Configuration
from .loca_config import (
    LOCAConfig,
    get_loca_config,
    reset_loca_config,
    get_config_summary,
    validate_configuration
)

# 🔧 Dependency Injection
from .di_container import (
    LOCAContainer,
    get_container,
    initialize_container,
    reset_container,
    get_container_info,
    validate_container
)

# 🎯 Common Types
from ._types import (
    DeploymentEnvironment,
    LogLevel,
    ServiceStatus,
    ConfigValidationResult,
    ConfigurationError,
    MissingConfigurationError,
    InvalidConfigurationError
)

# 📁 Domain Configs (for direct access if needed)
from . import configs

# 🎯 Public API - 외부에서 사용할 수 있는 인터페이스
__all__ = [
    # 🏆 Master Configuration
    "LOCAConfig",
    "get_loca_config",
    "reset_loca_config",
    "get_config_summary",
    "validate_configuration",

    # 🔧 Dependency Injection
    "LOCAContainer",
    "get_container",
    "initialize_container",
    "reset_container",
    "get_container_info",
    "validate_container",

    # 🎯 Common Types
    "DeploymentEnvironment",
    "LogLevel",
    "ServiceStatus",
    "ConfigValidationResult",
    "ConfigurationError",
    "MissingConfigurationError",
    "InvalidConfigurationError",

    # 📁 Domain Configs
    "configs",
]

# 📊 Configuration Layer 메타데이터
__version__ = "2.0.0"
__description__ = "LOCA Configuration Layer - 통합 설정 관리"
__author__ = "LOCA Development Team"


def get_layer_info() -> dict:
    """Configuration Layer 정보 반환"""
    return {
        "layer": "Configuration",
        "version": __version__,
        "description": __description__,
        "author": __author__,
        "architecture": {
            "pattern": "Hexagonal Architecture + DDD",
            "master_config": "LOCAConfig",
            "di_container": "LOCAContainer",
            "domains": ["base", "infrastructure", "ai"]
        },
        "components": {
            "master_config": "LOCAConfig - 마스터 설정 관리자",
            "di_container": "LOCAContainer - 의존성 주입 컨테이너",
            "base_configs": "기본 시스템 설정 (AppConfig, EnvironmentConfig)",
            "infrastructure_configs": "인프라 설정 (DatabaseConfig, RedisConfig, MonitoringConfig)",
            "ai_configs": "AI/ML 설정 (LangChainConfig, LLMProviderConfig, ElasticsearchConfig)"
        },
        "features": {
            "lazy_loading": "필요시점에 설정 로드",
            "environment_based": "환경별 자동 설정 조정",
            "validation": "전체 설정 유효성 검사",
            "dependency_injection": "DI 컨테이너 통합",
            "health_checking": "설정 및 서비스 헬스체크",
            "singleton_pattern": "전역 단일 인스턴스"
        },
        "public_api": __all__
    }


def validate_configuration_layer() -> tuple[bool, dict]:
    """
    🔍 Configuration Layer 전체 유효성 검사

    Returns:
        tuple[bool, dict]: (성공 여부, 검증 결과)
    """
    validation_result = {
        "layer_info": get_layer_info(),
        "master_config": {"valid": False},
        "di_container": {"valid": False},
        "domain_configs": {"valid": False},
        "overall_valid": False
    }

    try:
        # 1. 마스터 설정 검증
        is_config_valid, config_results = validate_configuration()
        validation_result["master_config"] = {
            "valid": is_config_valid,
            "details": config_results
        }

        # 2. DI 컨테이너 검증
        is_container_valid, container_results = validate_container()
        validation_result["di_container"] = {
            "valid": is_container_valid,
            "details": container_results
        }

        # 3. 도메인별 설정 검증
        from .configs import validate_all_domain_configs

        # 환경 설정을 가져와서 도메인 검증
        config = get_loca_config()
        domain_results = validate_all_domain_configs(config.deployment_env)
        validation_result["domain_configs"] = domain_results

        # 4. 전체 유효성 결정
        validation_result["overall_valid"] = all([
            is_config_valid,
            is_container_valid,
            domain_results.get("overall_valid", False)
        ])

        return validation_result["overall_valid"], validation_result

    except Exception as e:
        validation_result["validation_error"] = {
            "error": str(e),
            "error_type": type(e).__name__
        }
        return False, validation_result


async def check_configuration_layer_health() -> dict:
    """
    🏥 Configuration Layer 헬스체크

    모든 설정과 관련 서비스들의 상태를 확인합니다.
    """
    health_result = {
        "layer": "Configuration",
        "overall_healthy": False,
        "checks": {},
        "summary": {
            "total_checks": 0,
            "healthy_checks": 0,
            "unhealthy_checks": 0
        }
    }

    try:
        # 1. 설정 검증 상태
        is_valid, validation_details = validate_configuration_layer()
        health_result["checks"]["configuration_validation"] = {
            "status": "healthy" if is_valid else "unhealthy",
            "details": validation_details
        }

        # 2. 서비스 헬스체크
        from .configs import check_all_services_health
        services_health = await check_all_services_health()
        health_result["checks"]["services_health"] = {
            "status": "healthy" if services_health.get("overall_healthy", False) else "unhealthy",
            "details": services_health
        }

        # 3. 요약 계산
        healthy_checks = sum(
            1 for check in health_result["checks"].values()
            if check["status"] == "healthy"
        )
        total_checks = len(health_result["checks"])

        health_result["summary"] = {
            "total_checks": total_checks,
            "healthy_checks": healthy_checks,
            "unhealthy_checks": total_checks - healthy_checks
        }

        health_result["overall_healthy"] = health_result["summary"]["unhealthy_checks"] == 0

    except Exception as e:
        health_result["error"] = {
            "message": str(e),
            "error_type": type(e).__name__
        }
        health_result["overall_healthy"] = False

    return health_result


# 🚀 Layer 초기화 및 자동 검증
def initialize_configuration_layer() -> tuple[bool, dict]:
    """
    🚀 Configuration Layer 전체 초기화

    애플리케이션 시작 시 호출하여 전체 설정을 준비합니다.

    Returns:
        tuple[bool, dict]: (성공 여부, 초기화 결과)
    """
    initialization_result = {
        "layer": "Configuration",
        "initialized": False,
        "steps": {},
        "final_status": {}
    }

    try:
        # 1. 마스터 설정 초기화
        config = get_loca_config()
        initialization_result["steps"]["master_config"] = {
            "status": "success",
            "system_info": config.get_system_info()
        }

        # 2. DI 컨테이너 초기화
        container = initialize_container()
        initialization_result["steps"]["di_container"] = {
            "status": "success",
            "container_info": get_container_info()
        }

        # 3. 전체 검증
        is_valid, validation_results = validate_configuration_layer()
        initialization_result["steps"]["validation"] = {
            "status": "success" if is_valid else "failed",
            "results": validation_results
        }

        # 4. 최종 상태 설정
        initialization_result["initialized"] = is_valid
        initialization_result["final_status"] = {
            "config_summary": get_config_summary(),
            "layer_info": get_layer_info()
        }

        return is_valid, initialization_result

    except Exception as e:
        initialization_result["error"] = {
            "message": str(e),
            "error_type": type(e).__name__
        }
        return False, initialization_result


# 📋 자동 검증 설정 (환경 변수 기반)
import os
if os.getenv("LOCA_AUTO_VALIDATE_CONFIG", "false").lower() == "true":
    try:
        is_valid, results = validate_configuration_layer()
        if not is_valid:
            import warnings
            warnings.warn(
                f"Configuration Layer validation issues detected: {results}",
                UserWarning
            )
    except Exception as e:
        import warnings
        warnings.warn(
            f"Configuration Layer auto-validation failed: {e}",
            UserWarning
        )