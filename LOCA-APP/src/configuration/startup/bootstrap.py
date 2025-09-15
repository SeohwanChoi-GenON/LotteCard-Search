"""
애플리케이션 부트스트랩 유틸리티
main.py에서 사용할 수 있는 간단한 초기화 헬퍼 함수들을 제공합니다.
"""
import logging
from typing import Optional

from configuration.settings.app_settings import AppSettings


logger = logging.getLogger(__name__)


def setup_application_logging(settings: AppSettings) -> None:
    """
    애플리케이션 로깅을 설정합니다.
    main.py의 기본 로깅 설정을 보완합니다.
    """
    # 기본 로깅은 main.py에서 이미 설정되므로, 추가적인 설정만 수행

    # 외부 라이브러리 로그 레벨 조정
    external_loggers = [
        'httpx',
        'elasticsearch',
        'urllib3',
        'sqlalchemy.engine',
        'langchain'
    ]

    for logger_name in external_loggers:
        external_logger = logging.getLogger(logger_name)
        external_logger.setLevel(logging.WARNING)

    # 개발 환경에서는 더 상세한 로깅
    if settings.DEBUG:
        logging.getLogger('configuration').setLevel(logging.DEBUG)
        logging.getLogger('application').setLevel(logging.DEBUG)
        logging.getLogger('domain').setLevel(logging.DEBUG)
        logging.getLogger('infrastructure').setLevel(logging.DEBUG)

    logger.info("Enhanced logging configuration applied")


def validate_configuration(settings: AppSettings) -> None:
    """
    애플리케이션 설정을 검증합니다.
    필수 설정 누락이나 잘못된 값을 확인합니다.
    """
    validation_errors = []

    # 필수 설정 확인
    if not settings.APP_NAME:
        validation_errors.append("APP_NAME is required")

    if settings.PORT <= 0 or settings.PORT > 65535:
        validation_errors.append("PORT must be between 1 and 65535")

    if settings.WORKERS < 1:
        validation_errors.append("WORKERS must be at least 1")

    # Elasticsearch 설정 확인 (개발 환경이 아닐 때만)
    if not settings.DEBUG:
        if not settings.ELASTICSEARCH_HOST:
            validation_errors.append("ELASTICSEARCH_HOST is required in production")
        if not settings.ELASTICSEARCH_PORT:
            validation_errors.append("ELASTICSEARCH_PORT is required in production")

    if validation_errors:
        error_msg = "Configuration validation failed:\n" + "\n".join(f"- {error}" for error in validation_errors)
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info("Configuration validation passed")


def check_external_dependencies(settings: AppSettings) -> Optional[dict]:
    """
    외부 의존성 상태를 확인합니다.
    개발 환경에서는 경고만 출력하고, 프로덕션에서는 필수 검사를 수행합니다.

    Returns:
        dict: 각 서비스의 상태 정보
    """
    dependency_status = {
        'elasticsearch': False,
        'llm_service': False
    }

    try:
        # Elasticsearch 연결 체크 (간단한 버전)
        if settings.ELASTICSEARCH_HOST and settings.ELASTICSEARCH_PORT:
            # 실제 연결 테스트는 하지 않고, 설정만 확인
            dependency_status['elasticsearch'] = True
            logger.info("Elasticsearch configuration found")
        else:
            logger.warning("Elasticsearch configuration missing")

    except Exception as e:
        logger.warning(f"Elasticsearch check failed: {e}")

    try:
        # LLM 서비스 설정 체크
        if settings.LLM_API_BASE or settings.LLM_MODEL_NAME:
            dependency_status['llm_service'] = True
            logger.info("LLM service configuration found")
        else:
            logger.warning("LLM service configuration missing")

    except Exception as e:
        logger.warning(f"LLM service check failed: {e}")

    # 프로덕션 환경에서는 필수 의존성 확인
    if not settings.DEBUG:
        missing_services = [service for service, available in dependency_status.items() if not available]
        if missing_services:
            error_msg = f"Required services unavailable in production: {missing_services}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    logger.info(f"Dependency check completed: {dependency_status}")
    return dependency_status


def initialize_application_context(settings: AppSettings) -> dict:
    """
    애플리케이션 컨텍스트를 초기화합니다.
    main.py에서 호출하여 추가적인 초기화 작업을 수행합니다.

    Returns:
        dict: 초기화 결과와 상태 정보
    """
    logger.info("Initializing application context...")

    context = {
        'environment': 'development' if settings.DEBUG else 'production',
        'app_name': settings.APP_NAME,
        'app_version': settings.APP_VERSION,
        'initialized_at': None,
        'dependencies': {}
    }

    try:
        # 1. 로깅 설정 보완
        setup_application_logging(settings)

        # 2. 설정 검증
        validate_configuration(settings)

        # 3. 외부 의존성 확인
        dependencies = check_external_dependencies(settings)
        context['dependencies'] = dependencies

        # 4. 초기화 완료 시간 기록
        from datetime import datetime
        context['initialized_at'] = datetime.now().isoformat()

        logger.info(f"Application context initialized successfully in {context['environment']} mode")
        return context

    except Exception as e:
        logger.error(f"Failed to initialize application context: {e}")
        raise


def print_startup_banner(settings: AppSettings, context: dict) -> None:
    """
    애플리케이션 시작 시 배너를 출력합니다.
    """
    banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                            {settings.APP_NAME} v{settings.APP_VERSION}                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Environment: {context['environment']:<60} ║
║ Debug Mode:  {settings.DEBUG:<60} ║
║ Host:        {settings.HOST}:{settings.PORT}                                    ║
║ Workers:     {settings.WORKERS:<60} ║
║ Docs URL:    {settings.DOCS_URL if settings.DEBUG else 'Disabled':<60} ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Dependencies:                                                                ║
║   Elasticsearch: {'✓' if context['dependencies'].get('elasticsearch') else '✗':<56} ║
║   LLM Service:   {'✓' if context['dependencies'].get('llm_service') else '✗':<56} ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


# main.py에서 사용할 수 있는 간편 함수
def bootstrap_application(settings: AppSettings) -> dict:
    """
    main.py에서 호출할 수 있는 통합 부트스트랩 함수

    Usage in main.py:
        from configuration.startup.bootstrap import bootstrap_application

        def create_application():
            settings = get_settings()
            context = bootstrap_application(settings)  # 추가
            init_container(settings)
            app = create_app(settings)
            return app
    """
    context = initialize_application_context(settings)
    print_startup_banner(settings, context)
    return context


# 개발 편의를 위한 헬퍼 함수들
def get_health_info(settings: AppSettings) -> dict:
    """애플리케이션 상태 정보를 반환합니다."""
    return {
        'status': 'healthy',
        'app_name': settings.APP_NAME,
        'version': settings.APP_VERSION,
        'environment': 'development' if settings.DEBUG else 'production',
        'debug': settings.DEBUG
    }


def graceful_shutdown_handler():
    """애플리케이션 종료 시 정리 작업"""
    logger.info("Graceful shutdown initiated...")
    # 필요시 정리 작업 추가
    logger.info("Shutdown complete")