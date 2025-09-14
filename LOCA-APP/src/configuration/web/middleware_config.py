from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

from configuration.settings.app_settings import AppSettings

logger = logging.getLogger(__name__)


def configure_middleware(app: FastAPI, settings: AppSettings) -> None:
    """미들웨어 설정"""

    # CORS 미들웨어
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # 요청 로깅 미들웨어 (개발환경에서만)
    if settings.DEBUG:
        @app.middleware("http")
        async def log_requests(request, call_next):
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            logger.info(
                f"{request.method} {request.url.path} - "
                f"Status: {response.status_code} - "
                f"Time: {process_time:.3f}s"
            )
            return response

    logger.info("Middleware configuration completed")