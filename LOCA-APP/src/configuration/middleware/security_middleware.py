"""보안 관련 미들웨어"""
from fastapi import Request, Response
from .base_middleware import BaseCustomMiddleware


class SecurityHeadersMiddleware(BaseCustomMiddleware):
    """보안 헤더 추가 미들웨어"""

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # 보안 헤더 추가
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


class RateLimitMiddleware(BaseCustomMiddleware):
    """속도 제한 미들웨어 (향후 구현)"""

    async def dispatch(self, request: Request, call_next) -> Response:
        # TODO: Redis 기반 속도 제한 구현
        return await call_next(request)