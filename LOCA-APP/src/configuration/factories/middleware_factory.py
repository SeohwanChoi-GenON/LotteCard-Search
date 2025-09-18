import time
import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from ..settings.app_settings import AppSettings

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        # 요청 처리
        response = await call_next(request)

        # 처리 시간 계산 및 로깅
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )

        return response


def setup_middlewares(app: FastAPI, settings: AppSettings) -> None:
    """미들웨어 설정"""

    # CORS 미들웨어
    _setup_cors_middleware(app, settings)

    # 요청 로깅 미들웨어 (개발환경에서만)
    if settings.DEBUG:
        _setup_logging_middleware(app)

    logger.info("Middleware configuration completed")


def _setup_cors_middleware(app: FastAPI, settings: AppSettings) -> None:
    """CORS 미들웨어 설정"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    logger.debug("CORS middleware configured")


def _setup_logging_middleware(app: FastAPI) -> None:
    """로깅 미들웨어 설정"""
    app.add_middleware(RequestLoggingMiddleware)
    logger.debug("Request logging middleware configured")
