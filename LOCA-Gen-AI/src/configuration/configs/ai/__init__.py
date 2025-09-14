"""
🤖 AI Configuration Domain

AI/ML 관련 설정들을 관리하는 도메인입니다.

포함되는 설정:
- LangChainConfig: LangChain 프레임워크 설정
- LLMProviderConfig: LLM 서비스 제공자 설정
- ElasticsearchConfig: Elasticsearch 검색 엔진 설정
"""

from .langchain_config import LangChainConfig
from .llm_provider_config import LLMProviderConfig, LLMProvider, OpenAIModel
from .elasticsearch_config import ElasticsearchConfig

# 🎯 AI Domain Public API
__all__ = [
    "LangChainConfig",
    "LLMProviderConfig",
    "LLMProvider",
    "OpenAIModel",
    "ElasticsearchConfig",
]


def get_ai_config_info() -> dict:
    """AI 설정 도메인 정보"""
    return {
        "domain": "ai",
        "description": "AI/ML 관련 설정",
        "configs": {
            "LangChainConfig": {
                "description": "LangChain 프레임워크 설정",
                "responsibilities": [
                    "LangSmith 추적 설정",
                    "LangChain 캐시 설정",
                    "체인 실행 설정",
                    "텍스트 분할 설정"
                ]
            },
            "LLMProviderConfig": {
                "description": "LLM 서비스 제공자 설정",
                "responsibilities": [
                    "OpenAI API 설정",
                    "모델 선택 및 파라미터",
                    "토큰 관리 설정",
                    "스트리밍 설정"
                ]
            },
            "ElasticsearchConfig": {
                "description": "Elasticsearch 검색 설정",
                "responsibilities": [
                    "ES 클러스터 연결 설정",
                    "인덱스 관리 설정",
                    "하이브리드 검색 전략",
                    "벡터 검색 설정"
                ]
            }
        }
    }


def validate_ai_configs(deployment_env) -> dict:
    """AI 도메인 설정들 유효성 검사"""
    results = {}

    # LangChainConfig 검증
    try:
        langchain_config = LangChainConfig(
            deployment_env=deployment_env,
            debug_mode=deployment_env.value in ["development", "local"]
        )
        results["LangChainConfig"] = {
            "valid": True,
            "tracing_enabled": langchain_config.langsmith_tracing_enabled,
            "cache_enabled": langchain_config.langchain_cache_enabled,
            "chain_config": langchain_config.get_chain_config()
        }
    except Exception as e:
        results["LangChainConfig"] = {
            "valid": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

    # LLMProviderConfig 검증
    try:
        llm_config = LLMProviderConfig(deployment_env=deployment_env)
        results["LLMProviderConfig"] = {
            "valid": True,
            "api_key_configured": bool(llm_config.openai_api_key),
            "default_model": llm_config.openai_default_model.value,
            "completion_params": llm_config.get_default_completion_params()
        }
    except Exception as e:
        results["LLMProviderConfig"] = {
            "valid": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

    # ElasticsearchConfig 검증
    try:
        es_config = ElasticsearchConfig(deployment_env=deployment_env)
        results["ElasticsearchConfig"] = {
            "valid": True,
            "hosts_configured": bool(es_config.elasticsearch_hosts),
            "ssl_enabled": es_config.elasticsearch_use_ssl,
            "hybrid_search_config": es_config.get_hybrid_search_config()
        }
    except Exception as e:
        results["ElasticsearchConfig"] = {
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


def create_ai_configs(deployment_env, **kwargs):
    """AI 도메인 설정들 생성 팩토리"""
    return {
        "langchain": LangChainConfig(
            deployment_env=deployment_env,
            debug_mode=kwargs.get("debug_mode", False)
        ),
        "llm_provider": LLMProviderConfig(
            deployment_env=deployment_env
        ),
        "elasticsearch": ElasticsearchConfig(
            deployment_env=deployment_env
        )
    }


async def check_ai_services_health() -> dict:
    """AI 서비스들의 헬스체크"""
    health_results = {
        "overall_healthy": False,
        "services": {}
    }

    # OpenAI API 헬스체크 (구현 예정)
    health_results["services"]["openai"] = {
        "status": "unknown",
        "message": "Health check not implemented",
        "response_time_ms": None,
        "rate_limit_remaining": None
    }

    # LangSmith 연결 확인 (구현 예정)
    health_results["services"]["langsmith"] = {
        "status": "unknown",
        "message": "Health check not implemented",
        "response_time_ms": None
    }

    # Elasticsearch 헬스체크 (구현 예정)
    health_results["services"]["elasticsearch"] = {
        "status": "unknown",
        "message": "Health check not implemented",
        "response_time_ms": None,
        "cluster_status": None
    }

    # 전체 상태 결정
    healthy_services = [
        service["status"] == "healthy"
        for service in health_results["services"].values()
    ]
    health_results["overall_healthy"] = all(healthy_services) if healthy_services else False

    return health_results


def validate_ai_api_keys() -> dict:
    """AI 서비스 API 키들 유효성 검사"""
    key_validation = {
        "overall_valid": False,
        "keys": {}
    }

    # OpenAI API Key 검증 (구현 예정)
    key_validation["keys"]["openai"] = {
        "configured": "unknown",
        "valid": "unknown",
        "quota_available": "unknown",
        "note": "Key validation not implemented"
    }

    # LangSmith API Key 검증 (구현 예정)
    key_validation["keys"]["langsmith"] = {
        "configured": "unknown",
        "valid": "unknown",
        "project_accessible": "unknown",
        "note": "Key validation not implemented"
    }

    # 전체 유효성 결정
    valid_keys = [
        key["valid"] == "valid"
        for key in key_validation["keys"].values()
    ]
    key_validation["overall_valid"] = all(valid_keys) if valid_keys else False

    return key_validation