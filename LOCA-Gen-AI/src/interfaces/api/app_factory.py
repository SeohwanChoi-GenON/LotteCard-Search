from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from interfaces.api.router_registry import RouterRegistry
from interfaces.api.v1.chat.chat_controller import chat_router
from interfaces.config.settings import get_settings


def create_app() -> FastAPI:
    """FastAPI 애플리케이션 팩토리"""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL
    )

    # 미들웨어 설정
    _configure_middleware(app, settings)

    # 라우터 등록
    _register_routers(app, settings)

    return app


def _configure_middleware(app: FastAPI, settings):
    """미들웨어 구성"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _register_routers(app: FastAPI, settings):
    """라우터 등록"""
    router_registry = RouterRegistry()
    router_registry.register(chat_router)

    for router in router_registry.get_registered_routers():
        app.include_router(router, prefix=settings.API_V1_PREFIX)