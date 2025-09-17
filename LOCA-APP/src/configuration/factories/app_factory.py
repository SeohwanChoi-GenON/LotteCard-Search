from fastapi import FastAPI
from typing import AsyncGenerator, Callable
import logging

from configuration.factories.middleware_factory import configure_middleware
from configuration.factories.router_factory import RouterRegistry
from configuration.settings.app_settings import AppSettings

logger = logging.getLogger()


def create_app(settings: AppSettings, lifespan: Callable[[FastAPI], AsyncGenerator[None, None]] = None) -> FastAPI:
    """FastAPI 애플리케이션 팩토리"""

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url=settings.DOCS_URL if settings.DEBUG else None,
        redoc_url=settings.REDOC_URL if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan  # lifespan 추가
    )

    # 미들웨어 설정
    configure_middleware(app, settings)

    # 라우터 등록
    _register_routers(app, settings)

    logger.info(f"FastAPI application created: {settings.APP_NAME} v{settings.APP_VERSION}")
    return app


def _register_routers(app: FastAPI, settings: AppSettings) -> None:
    """라우터 등록"""
    router_registry = RouterRegistry()
    router_registry.auto_register_from_configs()

    registered_count = 0
    for router in router_registry.get_routers():
        app.include_router(router, prefix=settings.API_V1_PREFIX)
        registered_count += 1

    logger.info(f"Registered {registered_count} routers with prefix: {settings.API_V1_PREFIX}")