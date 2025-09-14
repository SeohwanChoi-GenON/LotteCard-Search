"""
🏆 LOCA 의존성 주입 컨테이너

LOCAConfig를 기반으로 한 통합 DI 관리
"""
from dependency_injector import containers, providers
from typing import Optional

from .loca_config import get_loca_config, LOCAConfig
from ._types import ConfigurationError


class LOCAContainer(containers.DeclarativeContainer):
    """🏆 LOCA 마스터 DI 컨테이너"""

    # 🎯 마스터 설정 (싱글톤)
    master_config = providers.Singleton(get_loca_config)

    # 🏗️ 기본 설정들 (Lazy Loading)
    app_config = providers.Singleton(
        lambda config: config.app,
        config=master_config
    )

    environment_config = providers.Singleton(
        lambda config: config.environment,
        config=master_config
    )

    # 🔧 인프라 설정들
    database_config = providers.Singleton(
        lambda config: config.database,
        config=master_config
    )

    redis_config = providers.Singleton(
        lambda config: config.redis,
        config=master_config
    )

    monitoring_config = providers.Singleton(
        lambda config: config.monitoring,
        config=master_config
    )

    # 🤖 AI 설정들
    langchain_config = providers.Singleton(
        lambda config: config.langchain,
        config=master_config
    )

    llm_provider_config = providers.Singleton(
        lambda config: config.llm_provider,
        config=master_config
    )

    elasticsearch_config = providers.Singleton(
        lambda config: config.elasticsearch,
        config=master_config
    )

    # 🚀 Application Layer - Use Cases (Primary Ports)
    # 실제 구현 시 아래 주석을 해제하고 구현
    # chat_use_case = providers.Factory(
    #     "application.use_cases.chat_use_case.ChatUseCase",
    #     master_config=master_config
    # )

    # workflow_orchestration_use_case = providers.Factory(
    #     "application.use_cases.workflow_orchestration_use_case.WorkflowOrchestrationUseCase",
    #     master_config=master_config
    # )

    # 🔌 Infrastructure Layer - Secondary Adapters
    # SQL Repository Adapters
    # sql_user_repository = providers.Singleton(
    #     "infrastructure.adapters.secondary.sql.sql_user_repository.SqlUserRepository",
    #     database_config=database_config
    # )

    # Redis Adapters
    # redis_cache_adapter = providers.Singleton(
    #     "infrastructure.adapters.secondary.redis.redis_cache_adapter.RedisCacheAdapter",
    #     redis_config=redis_config
    # )

    # HTTP Client Adapters
    # openai_llm_adapter = providers.Singleton(
    #     "infrastructure.adapters.secondary.openai.openai_llm_adapter.OpenAILLMAdapter",
    #     llm_provider_config=llm_provider_config
    # )

    # elasticsearch_search_adapter = providers.Singleton(
    #     "infrastructure.adapters.secondary.elasticsearch.elasticsearch_search_adapter.ElasticsearchSearchAdapter",
    #     elasticsearch_config=elasticsearch_config
    # )


# 🌍 글로벌 컨테이너 인스턴스
_container_instance: Optional[LOCAContainer] = None


def get_container() -> LOCAContainer:
    """🎯 DI 컨테이너 싱글톤 인스턴스 반환"""
    global _container_instance

    if _container_instance is None:
        _container_instance = LOCAContainer()

    return _container_instance


def initialize_container() -> LOCAContainer:
    """
    🚀 컨테이너 초기화 및 설정 검증

    애플리케이션 시작 시 호출하여 모든 설정을 검증하고
    DI 컨테이너를 준비상태로 만듭니다.

    Returns:
        LOCAContainer: 초기화된 컨테이너

    Raises:
        ConfigurationError: 설정 검증 실패 시
    """
    container = get_container()

    try:
        # 마스터 설정 가져오기 및 검증
        master_config = container.master_config()
        is_valid, validation_results = master_config.validate_all_configs()

        if not is_valid:
            error_details = {
                k: v for k, v in validation_results.items()
                if isinstance(v, dict) and not v.get('valid', False)
            }
            raise ConfigurationError(
                f"Container initialization failed - configuration validation errors: {error_details}",
                details=validation_results
            )

        # 기본 설정들 사전 로드 (Eager Loading)
        container.app_config()
        container.environment_config()

        return container

    except Exception as e:
        if isinstance(e, ConfigurationError):
            raise
        else:
            raise ConfigurationError(
                f"Container initialization failed: {str(e)}",
                details={"initialization_error": str(e)}
            )


def reset_container():
    """
    🔄 테스트용: 컨테이너 인스턴스 리셋
    주로 단위 테스트에서 사용
    """
    global _container_instance
    _container_instance = None


def get_container_info() -> dict:
    """
    📊 컨테이너 정보 반환
    디버깅 및 모니터링 용도
    """
    try:
        container = get_container()
        master_config = container.master_config()

        return {
            "container_initialized": True,
            "master_config_loaded": master_config is not None,
            "system_info": master_config.get_system_info() if master_config else None,
            "active_features": master_config.get_active_features() if master_config else None,
            "configuration_valid": master_config.validate_all_configs()[0] if master_config else False
        }

    except Exception as e:
        return {
            "container_initialized": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def validate_container() -> tuple[bool, dict]:
    """
    🔍 컨테이너 및 설정 전체 유효성 검사

    Returns:
        tuple[bool, dict]: (성공 여부, 검증 결과)
    """
    try:
        container = initialize_container()
        master_config = container.master_config()
        is_valid, validation_results = master_config.validate_all_configs()

        return is_valid, {
            "container_validation": True,
            "configuration_validation": is_valid,
            "details": validation_results,
            "container_info": get_container_info()
        }

    except Exception as e:
        return False, {
            "container_validation": False,
            "error": str(e),
            "error_type": type(e).__name__
        }