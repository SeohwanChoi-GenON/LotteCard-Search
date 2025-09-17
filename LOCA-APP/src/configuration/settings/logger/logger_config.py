"""
중앙 집중식 로깅 설정 및 유틸리티
"""
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from functools import lru_cache


class LoggerFactory:
    """로거 팩토리 클래스"""

    _configured = False
    _loggers: Dict[str, logging.Logger] = {}

    @classmethod
    def configure_logging(
            cls,
            level: str = "INFO",
            log_format: Optional[str] = None,
            log_file: Optional[str] = None
    ) -> None:
        """전역 로깅 설정"""

        if cls._configured:
            return

        # 기본 로그 포맷
        if log_format is None:
            log_format = (
                '%(asctime)s - %(name)s - %(levelname)s - '
                '[%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s'
            )

        # 핸들러 설정
        handlers = [logging.StreamHandler(sys.stdout)]

        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            handlers.append(
                logging.FileHandler(log_file, encoding='utf-8')
            )

        # 루트 로거 설정
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format=log_format,
            handlers=handlers,
            force=True  # 기존 설정 덮어쓰기
        )

        cls._configured = True

    @classmethod
    def get_logger(cls, name: Optional[str] = None) -> logging.Logger:
        """로거 인스턴스 반환"""

        # 호출자의 모듈명을 자동으로 가져오기
        if name is None:
            import inspect
            frame = inspect.currentframe().f_back
            name = frame.f_globals.get('__name__', 'unknown')

        # 캐시된 로거가 있으면 반환
        if name in cls._loggers:
            return cls._loggers[name]

        # 새 로거 생성
        logger = logging.getLogger(name)
        cls._loggers[name] = logger

        return logger

    @classmethod
    def set_level(cls, level: str, logger_name: Optional[str] = None) -> None:
        """특정 로거의 레벨 설정"""
        if logger_name:
            logger = logging.getLogger(logger_name)
            logger.setLevel(getattr(logging, level.upper()))
        else:
            logging.getLogger().setLevel(getattr(logging, level.upper()))


# 편의 함수들
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """로거 인스턴스를 가져오는 편의 함수"""
    return LoggerFactory.get_logger(name)


def configure_logging(**kwargs) -> None:
    """로깅을 설정하는 편의 함수"""
    LoggerFactory.configure_logging(**kwargs)


# 전역 로거 인스턴스 (즉시 사용 가능)
logger = LoggerFactory.get_logger(__name__)