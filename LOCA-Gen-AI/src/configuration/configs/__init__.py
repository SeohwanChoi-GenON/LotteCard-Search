"""
📁 LOCA Configuration Modules

도메인별로 조직화된 하위 설정 모듈들입니다.

구조:
- base/: 기본 시스템 설정
- infrastructure/: 인프라스트럭처 관련 설정
- ai/: AI/ML 관련 설정

각 도메인의 설정들은 LOCAConfig에서 통합 관리됩니다.
"""

# 🎯 도메인별 설정 모듈 임포트
from . import base
from . import infrastructure
from . import ai

# 🔧 공통 타입 및 유틸리티
from .._types import DeploymentEnvironment, ConfigValidationResult

# 📋 하위 설정들의 Public API
__all__ = [
    # 도메인 모듈들
    "base",
    "infrastructure",
    "ai",

    # 공통 타입
    "DeploymentEnvironment",
    "ConfigValidationResult",
]


def get_available_config_domains() -> dict:
    """사용 가능한 설정 도메인들 반환"""
    return {
        "base": {
            "description": "기본 시스템 설정",
            "configs": ["AppConfig", "EnvironmentConfig"],
            "module": "configuration.configs.base",
            "info_function": "get_base_config_info",
            "validate_function": "validate_base_configs",
            "factory_function": "create_base_configs"
        },
        "infrastructure": {
            "description": "인프라스트럭처 설정",
            "configs": ["DatabaseConfig", "RedisConfig", "MonitoringConfig"],
            "module": "configuration.configs.infrastructure",
            "info_function": "get_infrastructure_config_info",
            "validate_function": "validate_infrastructure_configs",
            "factory_function": "create_infrastructure_configs"
        },
        "ai": {
            "description": "AI/ML 관련 설정",
            "configs": ["LangChainConfig", "LLMProviderConfig", "ElasticsearchConfig"],
            "module": "configuration.configs.ai",
            "info_function": "get_ai_config_info",
            "validate_function": "validate_ai_configs",
            "factory_function": "create_ai_configs"
        }
    }


def validate_all_domain_configs(deployment_env: DeploymentEnvironment) -> dict:
    """모든 도메인 설정들의 유효성 검사"""
    validation_results = {
        "overall_valid": False,
        "domains": {},
        "summary": {
            "total_domains": 0,
            "valid_domains": 0,
            "invalid_domains": 0
        }
    }

    try:
        # Base configs 검증
        validation_results["domains"]["base"] = base.validate_base_configs(deployment_env)

        # Infrastructure configs 검증
        validation_results["domains"]["infrastructure"] = infrastructure.validate_infrastructure_configs(deployment_env)

        # AI configs 검증
        validation_results["domains"]["ai"] = ai.validate_ai_configs(deployment_env)

        # 요약 정보 계산
        validation_results["summary"]["total_domains"] = len(validation_results["domains"])
        valid_domains = sum(1 for domain in validation_results["domains"].values() if domain.get("valid", False))
        validation_results["summary"]["valid_domains"] = valid_domains
        validation_results["summary"]["invalid_domains"] = validation_results["summary"]["total_domains"] - valid_domains

        # 전체 성공 여부
        validation_results["overall_valid"] = validation_results["summary"]["invalid_domains"] == 0

    except Exception as e:
        validation_results["validation_error"] = {
            "error": str(e),
            "error_type": type(e).__name__
        }
        validation_results["overall_valid"] = False

    return validation_results


def create_all_domain_configs(deployment_env: DeploymentEnvironment, **kwargs) -> dict:
    """모든 도메인 설정들 생성"""
    configs = {}

    try:
        # Base configs 생성
        configs["base"] = base.create_base_configs(
            deployment_env,
            debug_mode=kwargs.get("debug_mode", False)
        )

        # Infrastructure configs 생성
        configs["infrastructure"] = infrastructure.create_infrastructure_configs(
            deployment_env,
            enable_tracing=kwargs.get("enable_tracing", True)
        )

        # AI configs 생성
        configs["ai"] = ai.create_ai_configs(
            deployment_env,
            debug_mode=kwargs.get("debug_mode", False)
        )

    except Exception as e:
        raise RuntimeError(f"Failed to create domain configs: {e}")

    return configs


async def check_all_services_health() -> dict:
    """모든 서비스들의 헬스체크"""
    health_results = {
        "overall_healthy": False,
        "infrastructure": {},
        "ai_services": {},
        "summary": {
            "total_checks": 0,
            "healthy_checks": 0,
            "unhealthy_checks": 0
        }
    }

    try:
        # Infrastructure 헬스체크
        health_results["infrastructure"] = await infrastructure.check_infrastructure_health()

        # AI 서비스 헬스체크
        health_results["ai_services"] = await ai.check_ai_services_health()

        # 요약 계산
        infra_healthy = health_results["infrastructure"].get("overall_healthy", False)
        ai_healthy = health_results["ai_services"].get("overall_healthy", False)

        health_results["summary"]["total_checks"] = 2
        health_results["summary"]["healthy_checks"] = sum([infra_healthy, ai_healthy])
        health_results["summary"]["unhealthy_checks"] = 2 - health_results["summary"]["healthy_checks"]
        health_results["overall_healthy"] = health_results["summary"]["unhealthy_checks"] == 0

    except Exception as e:
        health_results["error"] = {
            "message": str(e),
            "error_type": type(e).__name__
        }
        health_results["overall_healthy"] = False

    return health_results


def get_configuration_layer_summary() -> dict:
    """Configuration Layer 전체 요약"""
    return {
        "layer": "Configuration",
        "version": "2.0.0",
        "domains": get_available_config_domains(),
        "features": {
            "domain_validation": True,
            "environment_based_config": True,
            "health_checking": True,
            "lazy_loading": True,
            "factory_patterns": True
        }
    }