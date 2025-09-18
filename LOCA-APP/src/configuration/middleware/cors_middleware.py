"""CORS 미들웨어 설정"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from ..settings.app_settings import AppSettings

logger = logging.getLogger(__name__)


class CORSConfig:
    """CORS 설정 클래스"""

    def __init__(self, settings: AppSettings):
        self.settings = settings

    def setup(self, app: FastAPI) -> None:
        """CORS 미들웨어 설정"""

        cors_config = self._get_cors_config()

        app.add_middleware(
            CORSMiddleware,
            **cors_config
        )

        logger.info(f"CORS middleware configured with origins: {cors_config['allow_origins']}")

    def _get_cors_config(self) -> dict:
        """CORS 설정 반환"""
        if self.settings.debug:
            # 개발 환경: 관대한 설정
            return {
                "allow_origins": ["*"],
                "allow_credentials": True,
                "allow_methods": ["*"],
                "allow_headers": ["*"],
            }
        else:
            # 운영 환경: 엄격한 설정
            return {
                "allow_origins": self.settings.allowed_origins,
                "allow_credentials": True,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": [
                    "Accept",
                    "Accept-Language",
                    "Content-Language",
                    "Content-Type",
                    "Authorization",
                    "X-Requested-With",
                    # Gateway 헤더들
                    "GUID",
                    "SRC_SYS_CD",
                    "STC_BIZ_CDD",
                    "GRAM_PRG_NO",
                    "GRAN_NO",
                    "TSMT"
                ],
            }