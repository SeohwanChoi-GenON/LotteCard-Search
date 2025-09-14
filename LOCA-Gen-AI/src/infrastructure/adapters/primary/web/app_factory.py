"""
🏭 FastAPI 애플리케이션 팩토리

헥사고날 아키텍처의 Primary Adapter 생성 및 구성을 담당합니다.
"""
import asyncio
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from configuration import get_loca_config, initialize_container, LOCAConfig
from .router_registry import RouterRegistry
# from .middleware import (
#     ErrorHandlingMiddleware,
#     RequestLoggingMiddleware,
#     RateLimitingMiddleware,
#     SecurityMiddleware,
# )
# from .startup import ApplicationInitializer


class WebApplicationFactory:
    """FastAPI 애플리케이션 생성 및 구성 관리"""

    def __init__(self, config: Optional[LOCAConfig] = None):
        self.config = config or get_loca_config()
        self.container = None
        self._app: Optional[FastAPI] = None
        self._initialization_results: Dict[str, Any] = {}

    async def create_application(self) -> FastAPI:
        """FastAPI 애플리케이션 생성"""
        if self._app is not None:
            return self._app

        print(f"🚀 Creating {self.config.system_name} FastAPI Application...")

        # 애플리케이션 라이프사이클 매니저
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # 시작 시
            await self._startup_event(app)
            yield
            # 종료 시
            await self._shutdown_event(app)

        # FastAPI 애플리케이션 생성
        self._app = FastAPI(
            title=self.config.app.api_title,
            version=self.config.system_version,
            description=self.config.system_description,
            docs_url=self.config.app.docs_url if self.config.environment.enable_swagger_ui else None,
            redoc_url=self.config.app.redoc_url if self.config.environment.enable_swagger_ui else None,
            openapi_url=self.config.app.openapi_url if self.config.environment.enable_swagger_ui else None,
            debug=self.config.debug_mode,
            lifespan=lifespan
        )

        # DI 컨테이너 초기화 및 바인딩
        await self._initialize_container()

        # 미들웨어 구성
        await self._configure_middleware()

        # Primary Adapter(컨트롤러) 등록
        await self._register_primary_adapters()

        # 예외 핸들러 등록
        self._register_exception_handlers()

        print(f"✅ {self.config.system_name} Application created successfully!")
        return self._app

    async def _initialize_container(self):
        """DI 컨테이너 초기화"""
        print("🔧 Initializing DI Container...")

        self.container = initialize_container()

        # FastAPI 앱에 컨테이너 바인딩
        self._app.container = self.container
        self._app.state.container = self.container
        self._app.state.config = self.config

        print("✅ DI Container initialized and bound to app")

    async def _configure_middleware(self):
        """미들웨어 구성 (순서 중요!)"""
        print("🛡️ Configuring middleware stack...")

        # 1. 보안 미들웨어 (최우선)
        if self.config.is_production():
            self._app.add_middleware(SecurityMiddleware, config=self.config.security)

            # 신뢰할 수 있는 호스트 (운영환경)
            trusted_hosts = self.config.security.trusted_hosts
            if trusted_hosts:
                self._app.add_middleware(
                    TrustedHostMiddleware,
                    allowed_hosts=trusted_hosts
                )

        # 2. 에러 핸들링 미들웨어
        self._app.add_middleware(ErrorHandlingMiddleware, config=self.config)

        # 3. 요청 로깅 미들웨어
        if self.config.monitoring.enable_request_logging:
            self._app.add_middleware(
                RequestLoggingMiddleware,
                config=self.config.monitoring
            )

        # 4. 레이트 리미팅 미들웨어
        if self.config.environment.rate_limit_enabled:
            self._app.add_middleware(
                RateLimitingMiddleware,
                requests_per_minute=self.config.environment.rate_limit_per_minute
            )

        # 5. CORS 미들웨어 (가장 마지막)
        await self._configure_cors_middleware()

        print("✅ Middleware stack configured")

    async def _configure_cors_middleware(self):
        """CORS 미들웨어 구성"""
        cors_config = self.config.security.get_cors_config()

        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_config.allowed_origins,
            allow_credentials=cors_config.allow_credentials,
            allow_methods=cors_config.allowed_methods,
            allow_headers=cors_config.allowed_headers,
            expose_headers=cors_config.expose_headers,
            max_age=cors_config.max_age
        )

        print(f"✅ CORS configured for origins: {cors_config.allowed_origins}")

    async def _register_primary_adapters(self):
        """Primary Adapter(컨트롤러) 등록"""
        print("🎯 Registering Primary Adapters (Controllers)...")

        # 라우터 레지스트리 초기화
        router_registry = RouterRegistry(self.config, self.container)

        # 컨트롤러들 자동 스캔 및 등록
        registered_controllers = await router_registry.register_all_controllers()

        # API 접두사 적용하여 라우터들 등록
        api_prefix = self.config.app.api_prefix
        for controller_info in registered_controllers:
            self._app.include_router(
                controller_info.router,
                prefix=api_prefix + controller_info.prefix,
                tags=controller_info.tags
            )

            print(f"✅ Registered: {controller_info.name} -> {api_prefix}{controller_info.prefix}")

        total_routes = len([route for route in self._app.routes])
        print(f"✅ Total {total_routes} routes registered from {len(registered_controllers)} controllers")

    def _register_exception_handlers(self):
        """예외 핸들러 등록"""
        print("⚠️ Registering exception handlers...")

        @self._app.exception_handler(StarletteHTTPException)
        async def http_exception_handler(request: Request, exc: StarletteHTTPException):
            """HTTP 예외 핸들러"""
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "type": "http_error",
                        "status_code": exc.status_code,
                        "message": exc.detail,
                        "path": str(request.url.path),
                        "method": request.method,
                        "timestamp": self._get_current_timestamp()
                    }
                }
            )

        @self._app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            """요청 검증 예외 핸들러"""
            return JSONResponse(
                status_code=422,
                content={
                    "error": {
                        "type": "validation_error",
                        "status_code": 422,
                        "message": "Request validation failed",
                        "details": exc.errors(),
                        "path": str(request.url.path),
                        "method": request.method,
                        "timestamp": self._get_current_timestamp()
                    }
                }
            )

        print("✅ Exception handlers registered")

    async def _startup_event(self, app: FastAPI):
        """애플리케이션 시작 이벤트"""
        print("🚀 Application startup initiated...")

        # 애플리케이션 초기화
        initializer = ApplicationInitializer(self.config, self.container)
        self._initialization_results = await initializer.initialize_application()

        # 초기화 결과를 앱 상태에 저장
        app.state.initialization_results = self._initialization_results
        app.state.startup_time = self._get_current_timestamp()

        startup_status = "✅ SUCCESS" if self._initialization_results.get("overall_success") else "⚠️ WITH ISSUES"
        print(f"🎯 Application startup completed: {startup_status}")

    async def _shutdown_event(self, app: FastAPI):
        """애플리케이션 종료 이벤트"""
        print("🛑 Application shutdown initiated...")

        # 리소스 정리
        if hasattr(app.state, 'container') and app.state.container:
            try:
                if hasattr(app.state.container, 'shutdown'):
                    await app.state.container.shutdown()
            except Exception as e:
                print(f"⚠️ Error during container shutdown: {e}")

        print("✅ Application shutdown completed")

    def _get_current_timestamp(self) -> str:
        """현재 타임스탬프 반환"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"

    @property
    def app(self) -> Optional[FastAPI]:
        """FastAPI 앱 인스턴스 반환"""
        return self._app


# 팩토리 함수
async def create_app(config: Optional[LOCAConfig] = None) -> FastAPI:
    """
    🚀 LOCA FastAPI 애플리케이션 생성

    헥사고날 아키텍처 기반으로 Primary Adapter를 구성합니다.
    """
    factory = WebApplicationFactory(config)
    return await factory.create_application()


# 동기식 래퍼 함수 (기존 호환성)
def create_app_sync(config: Optional[LOCAConfig] = None) -> FastAPI:
    """동기식 앱 생성 래퍼"""
    return asyncio.run(create_app(config))