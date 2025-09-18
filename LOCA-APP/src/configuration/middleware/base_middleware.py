"""미들웨어 베이스 클래스"""
from abc import ABC, abstractmethod
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from ..settings.app import AppSettings

logger = logging.getLogger(__name__)


class BaseCustomMiddleware(BaseHTTPMiddleware, ABC):
    """커스텀 미들웨어 베이스 클래스"""

    def __init__(self, app, settings: AppSettings):
        super().__init__(app)
        self.settings = settings
        self.logger = logger

    @abstractmethod
    async def dispatch(self, request: Request, call_next) -> Response:
        """미들웨어 처리 로직 (하위 클래스에서 구현)"""
        pass

    def should_skip_request(self, request: Request) -> bool:
        """특정 경로는 미들웨어 처리에서 제외"""
        skip_paths = ['/health', '/metrics', '/favicon.ico']
        return request.url.path in skip_paths
