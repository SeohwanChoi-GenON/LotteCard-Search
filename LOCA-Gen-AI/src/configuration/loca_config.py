"""
🏆 LOCA 시스템 통합 설정 관리자 (Master Configuration)

스프링부트 스타일의 Profile 기반 환경 파일 자동 로딩
"""
import os
from typing import Optional, Dict, Any, List
from pathlib import Path
from pydantic import Field, ConfigDict, validator
from pydantic_settings import BaseSettings

from ._types import DeploymentEnvironment, ConfigurationError
from .configs.base.app_config import AppConfig
from .configs.base.environment_config import EnvironmentConfig
from .configs.infrastructure.database_config import DatabaseConfig
from .configs.infrastructure.redis_config import RedisConfig
from .configs.infrastructure.monitoring_config import MonitoringConfig
from .configs.ai.langchain_config import LangChainConfig
from .configs.ai.llm_provider_config import LLMProviderConfig
from .configs.ai.elasticsearch_config import ElasticsearchConfig


def get_active_profiles() -> List[str]:
    """
    🎯 스프링부트 스타일: Active Profiles 감지

    우선순위:
    1. LOCA_PROFILES_ACTIVE 환경변수 (쉼표로 구분)
    2. LOCA_DEPLOYMENT_ENV 환경변수
    3. 자동 감지 (CI, 개발환경 등)
    4. 기본값: dev
    """
    # 1. 명시적 프로파일 설정
    profiles_env = os.getenv("LOCA_PROFILES_ACTIVE", "").strip()
    if profiles_env:
        return [p.strip() for p in profiles_env.split(",")]

    # 2. 배포 환경 기반
    deployment_env = os.getenv("LOCA_DEPLOYMENT_ENV", "").lower()
    if deployment_env:
        # 매핑: deployment_env -> profile
        env_mapping = {
            "development": "dev",
            "local": "local",
            "staging": "stage",
            "production": "prod",
            "test": "test"
        }
        if deployment_env in env_mapping:
            return [env_mapping[deployment_env]]

    # 3. 자동 감지
    if os.getenv("CI") or os.getenv("GITHUB_ACTIONS"):
        return ["test"]

    if os.getenv("KUBERNETES_SERVICE_HOST"):  # K8s 환경
        return ["prod"]

    # 4. 기본값
    return ["dev"]


def build_env_files_from_profiles(profiles: List[str]) -> List[str]:
    """
    🎯 프로파일 기반 환경 파일 목록 구성

    로딩 순서 (늦게 로드될수록 우선순위 높음):
    1. .env (기본 설정)
    2. .env.{profile} (프로파일별 설정) - 프로파일 순서대로
    3. .env.local (로컬 오버라이드, prod가 아닐 때만)
    """
    PROJECT_ROOT = Path(__file__).parent.parent
    env_files = []

    # 1. 기본 파일 (.env)
    base_file = PROJECT_ROOT / ".env"
    if base_file.exists():
        env_files.append(str(base_file))

    # 2. 프로파일별 파일들 (.env.{profile})
    for profile in profiles:
        profile_file = PROJECT_ROOT / f".env.{profile}"
        if profile_file.exists():
            env_files.append(str(profile_file))

    # 3. 로컬 오버라이드 (.env.local) - 운영환경이 아닐 때만
    if "prod" not in profiles:
        local_file = PROJECT_ROOT / ".env.local"
        if local_file.exists():
            env_files.append(str(local_file))

    return env_files


# 🎯 Active Profiles & Environment Files 자동 구성
ACTIVE_PROFILES = get_active_profiles()
ENV_FILES = build_env_files_from_profiles(ACTIVE_PROFILES)


class LOCAConfig(BaseSettings):
    """
    🏆 LOCA 시스템 마스터 설정 클래스 (Spring Boot Style)

    Profile 기반 자동 환경 파일 로딩:
    - dev: .env + .env.dev + .env.local
    - prod: .env + .env.prod
    - stage: .env + .env.stage + .env.local
    - test: .env + .env.test + .env.local
    """

    model_config = ConfigDict(
        env_file=ENV_FILES,  # 🎯 Profile 기반 자동 구성
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        use_enum_values=True
    )

    # 🌍 시스템 메타 정보
    system_name: str = Field("LOCA-Gen-AI", env="LOCA_SYSTEM_NAME")
    system_version: str = Field("2.0.0", env="LOCA_SYSTEM_VERSION")
    system_description: str = Field("LOCA Generative AI ChatBot System", env="LOCA_SYSTEM_DESCRIPTION")

    # 🎯 프로파일 & 환경 설정
    active_profiles: List[str] = Field(default_factory=lambda: ACTIVE_PROFILES, env="LOCA_PROFILES_ACTIVE")
    deployment_env: DeploymentEnvironment = Field(
        DeploymentEnvironment.DEVELOPMENT,
        env="LOCA_DEPLOYMENT_ENV"
    )

    # 🔧 시스템 레벨 설정
    debug_mode: bool = Field(False, env="LOCA_DEBUG")
    profile_enabled: bool = Field(False, env="LOCA_PROFILE_ENABLED")
    health_check_enabled: bool = Field(True, env="LOCA_HEALTH_CHECK_ENABLED")

    # 🌐 API 서버 설정
    api_host: str = Field("127.0.0.1", env="LOCA_API_HOST")
    api_port: int = Field(8000, env="LOCA_API_PORT")
    workers: int = Field(1, env="LOCA_WORKERS")

    # 🔧 기능 활성화 설정
    enable_debug_endpoints: bool = Field(True, env="LOCA_ENABLE_DEBUG_ENDPOINTS")
    enable_experimental: bool = Field(True, env="LOCA_ENABLE_EXPERIMENTAL")
    enable_swagger_ui: bool = Field(True, env="LOCA_ENABLE_SWAGGER_UI")

    # 📊 로깅 및 모니터링 설정
    log_level: str = Field("INFO", env="LOCA_LOG_LEVEL")
    enable_request_tracing: bool = Field(True, env="LOCA_ENABLE_TRACING")
    db_echo_sql: bool = Field(False, env="LOCA_DB_ECHO_SQL")
    metrics_enabled: bool = Field(True, env="LOCA_METRICS_ENABLED")

    # 🔐 보안 설정
    secret_key: str = Field(..., env="LOCA_SECRET_KEY")
    cors_origins: List[str] = Field(default_factory=lambda: ["*"], env="LOCA_CORS_ORIGINS")

    # 🗄️ 데이터베이스 설정
    database_url: str = Field(..., env="LOCA_DATABASE_URL")

    # 🔴 Redis 설정
    redis_url: str = Field("redis://localhost:6379/0", env="LOCA_REDIS_URL")

    # 🤖 AI/LLM 설정
    openai_default_model: str = Field("gpt-3.5-turbo", env="LOCA_OPENAI_DEFAULT_MODEL")
    llm_temperature: float = Field(0.1, env="LOCA_LLM_TEMPERATURE")
    llm_enable_streaming: bool = Field(False, env="LOCA_LLM_ENABLE_STREAMING")

    # 🔍 Elasticsearch 설정
    es_hosts: List[str] = Field(default_factory=lambda: ["localhost:9200"], env="LOCA_ES_HOSTS")
    es_use_ssl: bool = Field(False, env="LOCA_ES_USE_SSL")
    es_verify_certs: bool = Field(False, env="LOCA_ES_VERIFY_CERTS")

    # 📈 LangChain 추적 설정
    langsmith_tracing_enabled: bool = Field(True, env="LANGSMITH_TRACING_ENABLED")
    langchain_verbose: bool = Field(True, env="LANGCHAIN_VERBOSE")
    langchain_debug: bool = Field(True, env="LANGCHAIN_DEBUG")

    # 🔧 기타 설정
    auto_validate_config: bool = Field(True, env="LOCA_AUTO_VALIDATE_CONFIG")

    # 🎛️ 하위 설정들 (Lazy Loading)
    _app_config: Optional[AppConfig] = None
    _environment_config: Optional[EnvironmentConfig] = None
    _database_config: Optional[DatabaseConfig] = None
    _redis_config: Optional[RedisConfig] = None
    _monitoring_config: Optional[MonitoringConfig] = None
    _langchain_config: Optional[LangChainConfig] = None
    _llm_provider_config: Optional[LLMProviderConfig] = None
    _elasticsearch_config: Optional[ElasticsearchConfig] = None

    @validator('active_profiles', pre=True)
    def validate_active_profiles(cls, v):
        """Active Profiles 파싱"""
        if isinstance(v, str):
            return [p.strip() for p in v.split(',') if p.strip()]
        return v if v else ["dev"]

    @validator('deployment_env', pre=True)
    def validate_deployment_env(cls, v):
        """배포 환경 유효성 검사"""
        if isinstance(v, str):
            return DeploymentEnvironment(v.lower())
        return v

    @validator('cors_origins', pre=True)
    def validate_cors_origins(cls, v):
        """CORS Origins 파싱"""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(',')]
        return v

    @validator('es_hosts', pre=True)
    def validate_es_hosts(cls, v):
        """Elasticsearch hosts 파싱"""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [host.strip() for host in v.split(',')]
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 프로파일 기반 자동 설정 조정
        self._adjust_settings_by_profiles()

    def _adjust_settings_by_profiles(self):
        """프로파일 기반 설정 자동 조정"""
        if self.has_profile("dev") or self.has_profile("local"):
            # 개발/로컬 프로파일
            if not hasattr(self, '_debug_mode_set'):
                self.debug_mode = True
                self.profile_enabled = True
                self.log_level = "DEBUG"
                self._debug_mode_set = True

        elif self.has_profile("prod"):
            # 운영 프로파일
            self.debug_mode = False
            self.enable_debug_endpoints = False
            self.enable_experimental = False
            self.enable_swagger_ui = False
            self.log_level = "WARNING"

        elif self.has_profile("test"):
            # 테스트 프로파일
            self.debug_mode = True
            self.log_level = "DEBUG"
            self.health_check_enabled = False

    def has_profile(self, profile: str) -> bool:
        """특정 프로파일 활성화 여부 확인"""
        return profile in self.active_profiles

    def is_production_profile(self) -> bool:
        """운영 프로파일 여부"""
        return self.has_profile("prod")

    def is_development_profile(self) -> bool:
        """개발 프로파일 여부"""
        return self.has_profile("dev") or self.has_profile("local")

    def is_test_profile(self) -> bool:
        """테스트 프로파일 여부"""
        return self.has_profile("test")

    # 🔍 Profile & Environment Files 정보
    def get_profile_info(self) -> Dict[str, Any]:
        """프로파일 및 환경 파일 정보"""
        PROJECT_ROOT = Path(__file__).parent.parent

        return {
            "active_profiles": self.active_profiles,
            "deployment_env": self.deployment_env.value,
            "project_root": str(PROJECT_ROOT),
            "loaded_env_files": ENV_FILES,
            "profile_detection": {
                "LOCA_PROFILES_ACTIVE": os.getenv("LOCA_PROFILES_ACTIVE"),
                "LOCA_DEPLOYMENT_ENV": os.getenv("LOCA_DEPLOYMENT_ENV"),
                "auto_detected": not bool(os.getenv("LOCA_PROFILES_ACTIVE") or os.getenv("LOCA_DEPLOYMENT_ENV"))
            },
            "available_env_files": {
                ".env": (PROJECT_ROOT / ".env").exists(),
                ".env.dev": (PROJECT_ROOT / ".env.dev").exists(),
                ".env.prod": (PROJECT_ROOT / ".env.prod").exists(),
                ".env.stage": (PROJECT_ROOT / ".env.stage").exists(),
                ".env.test": (PROJECT_ROOT / ".env.test").exists(),
                ".env.local": (PROJECT_ROOT / ".env.local").exists(),
            }
        }

    # ... 기존의 모든 property 메서드들과 다른 메서드들은 그대로 유지 ...

    # 🏗️ 기본 설정 접근자들
    @property
    def app(self) -> AppConfig:
        """애플리케이션 기본 설정"""
        if self._app_config is None:
            self._app_config = AppConfig(
                deployment_env=self.deployment_env,
                debug_mode=self.debug_mode,
                api_host=self.api_host,
                api_port=self.api_port,
                workers=self.workers,
                enable_debug_endpoints=self.enable_debug_endpoints,
                enable_experimental=self.enable_experimental,
                enable_swagger_ui=self.enable_swagger_ui
            )
        return self._app_config

    @property
    def environment(self) -> EnvironmentConfig:
        """환경별 설정"""
        if self._environment_config is None:
            self._environment_config = EnvironmentConfig(
                deployment_env=self.deployment_env
            )
        return self._environment_config

    # 🔧 인프라 설정 접근자들
    @property
    def database(self) -> DatabaseConfig:
        """데이터베이스 설정"""
        if self._database_config is None:
            self._database_config = DatabaseConfig(
                deployment_env=self.deployment_env,
                database_url=self.database_url,
                echo_sql=self.db_echo_sql
            )
        return self._database_config

    @property
    def redis(self) -> RedisConfig:
        """Redis 설정"""
        if self._redis_config is None:
            self._redis_config = RedisConfig(
                deployment_env=self.deployment_env,
                redis_url=self.redis_url
            )
        return self._redis_config

    @property
    def monitoring(self) -> MonitoringConfig:
        """모니터링 설정"""
        if self._monitoring_config is None:
            self._monitoring_config = MonitoringConfig(
                deployment_env=self.deployment_env,
                enable_tracing=self.enable_request_tracing,
                metrics_enabled=self.metrics_enabled,
                log_level=self.log_level
            )
        return self._monitoring_config

    # 🤖 AI 설정 접근자들
    @property
    def langchain(self) -> LangChainConfig:
        """LangChain 설정"""
        if self._langchain_config is None:
            self._langchain_config = LangChainConfig(
                deployment_env=self.deployment_env,
                debug_mode=self.debug_mode,
                verbose=self.langchain_verbose,
                debug=self.langchain_debug,
                tracing_enabled=self.langsmith_tracing_enabled
            )
        return self._langchain_config

    @property
    def llm_provider(self) -> LLMProviderConfig:
        """LLM Provider 설정"""
        if self._llm_provider_config is None:
            self._llm_provider_config = LLMProviderConfig(
                deployment_env=self.deployment_env,
                default_model=self.openai_default_model,
                temperature=self.llm_temperature,
                enable_streaming=self.llm_enable_streaming
            )
        return self._llm_provider_config

    @property
    def elasticsearch(self) -> ElasticsearchConfig:
        """Elasticsearch 설정"""
        if self._elasticsearch_config is None:
            self._elasticsearch_config = ElasticsearchConfig(
                deployment_env=self.deployment_env,
                hosts=self.es_hosts,
                use_ssl=self.es_use_ssl,
                verify_certs=self.es_verify_certs
            )
        return self._elasticsearch_config

    # 🎯 환경별 판단 메서드들
    def is_production(self) -> bool:
        """운영 환경 여부"""
        return self.deployment_env == DeploymentEnvironment.PRODUCTION or self.has_profile("prod")

    def is_development(self) -> bool:
        """개발 환경 여부"""
        return (self.deployment_env in [DeploymentEnvironment.DEVELOPMENT, DeploymentEnvironment.LOCAL]
                or self.has_profile("dev") or self.has_profile("local"))

    def is_staging(self) -> bool:
        """스테이징 환경 여부"""
        return self.deployment_env == DeploymentEnvironment.STAGING or self.has_profile("stage")

    # 🔍 기존의 다른 메서드들도 그대로 유지...
    def validate_all_configs(self) -> tuple[bool, Dict[str, Any]]:
        """모든 하위 설정들의 유효성 검사"""
        # 기존 코드 그대로...
        pass

    def get_configuration_summary(self) -> Dict[str, Any]:
        """전체 설정 요약 (프로파일 정보 포함)"""
        base_summary = {
            'system_info': self.get_system_info(),
            'profile_info': self.get_profile_info(),  # 🎯 추가
            'active_features': self.get_active_features(),
            'config_validation': self.validate_all_configs()[0] if hasattr(self, 'validate_all_configs') else True,
        }
        return base_summary


# 🌍 글로벌 마스터 설정 인스턴스 - 기존과 동일
_loca_config_instance: Optional[LOCAConfig] = None


def get_loca_config() -> LOCAConfig:
    """🎯 LOCA 마스터 설정 싱글톤 인스턴스 반환"""
    global _loca_config_instance

    if _loca_config_instance is None:
        _loca_config_instance = LOCAConfig()

        if _loca_config_instance.auto_validate_config:
            is_valid, validation_results = _loca_config_instance.validate_all_configs()

            if not is_valid:
                error_details = {
                    k: v for k, v in validation_results.items()
                    if isinstance(v, dict) and not v.get('valid', False)
                }
                raise ConfigurationError(
                    f"LOCA Master Configuration validation failed: {error_details}"
                )

    return _loca_config_instance


def reset_loca_config():
    """🔄 테스트용: 마스터 설정 인스턴스 리셋"""
    global _loca_config_instance
    _loca_config_instance = None


def get_config_summary() -> Dict[str, Any]:
    """📊 설정 요약 정보 반환 (프로파일 정보 포함)"""
    try:
        config = get_loca_config()
        return config.get_configuration_summary()
    except Exception as e:
        return {
            'error': True,
            'message': str(e),
            'error_type': type(e).__name__
        }
