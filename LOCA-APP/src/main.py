import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from configuration.di_container import init_container, cleanup_container
from configuration.settings.app_settings import get_settings
from configuration.settings.constants import UvicornConfig
from configuration.settings.logger.logger_config import get_logger, configure_logging
from configuration.startup.bootstrap import bootstrap_application, cleanup_application
from configuration.factories.app_factory import create_app


logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    애플리케이션 라이프사이클 관리

    startup과 shutdown 이벤트를 관리합니다.
    """
    settings = get_settings()

    configure_logging(
        level="DEBUG" if settings.DEBUG else "INFO",
        log_file="app.log"
    )

    # 애플리케이션 시작 시 실행
    try:
        logger.info("Starting LOCA Chat API application...")

        # 부트스트랩 초기화
        context = bootstrap_application(settings)
        logger.info("Bootstrap initialization completed")

        # DI 컨테이너 초기화
        init_container(settings)
        logger.info("DI Container initialized")

        # 애플리케이션 상태를 factories.state에 저장
        app.state.context = context
        app.state.settings = settings

        logger.info("🎉 Application startup completed successfully")

    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        raise

    # yield 지점: 애플리케이션 실행 중
    yield

    # 애플리케이션 종료 시 실행
    try:
        logger.info("🔄 Shutting down LOCA Chat API application...")

        # 리소스 정리
        await cleanup_container()
        logger.info("DI Container cleaned up")

        # 부트스트랩 정리
        if hasattr(app.state, 'context'):
            await cleanup_application(app.state.context)
            logger.info("Application context cleaned up")

        logger.info("Application shutdown completed successfully")

    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        # shutdown 에러는 로그만 남기고 계속 진행


def create_application() -> FastAPI:
    """FastAPI 애플리케이션을 생성합니다."""
    settings = get_settings()

    # lifespan과 함께 앱 생성
    app = create_app(settings, lifespan=lifespan)

    return app


def _run_development_server(logger: logging.Logger) -> None:
    """개발 환경에서 서버를 실행합니다."""
    logger.info("Starting server in development mode with hot reload...")
    uvicorn.run(
        "main:app",
        host=UvicornConfig.HOST,
        port=UvicornConfig.PORT,
        log_level=UvicornConfig.LOG_LEVEL,
        timeout_keep_alive=UvicornConfig.TIMEOUT_KEEP_ALIVE,
        reload=True,
        reload_excludes=["*.log", "__pycache__", ".git"]  # 불필요한 reload 방지
    )


def _run_production_server(app: FastAPI, logger: logging.Logger) -> None:
    """프로덕션 환경에서 서버를 실행합니다."""
    logger.info("Starting server in production mode...")
    uvicorn.run(
        app=app,
        host=UvicornConfig.HOST,
        port=UvicornConfig.PORT,
        workers=UvicornConfig.WORKERS,
        log_level=UvicornConfig.LOG_LEVEL,
        timeout_keep_alive=UvicornConfig.TIMEOUT_KEEP_ALIVE
    )


def main() -> None:
    try:
        settings = get_settings()

        logger.info(f"Initializing {settings.APP_NAME} v{settings.APP_VERSION}")

        # 환경에 따른 서버 실행
        if settings.DEBUG:
            _run_development_server(logger)
        else:
            app = create_application()
            _run_production_server(app, logger)

    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise


# 개발 환경에서 hot reload를 위한 앱 인스턴스
app = create_application()


if __name__ == '__main__':
    main()