import logging
import sys
from pathlib import Path
from typing import Optional, Dict
from logging.handlers import RotatingFileHandler

from configuration.settings.logging_settings import LoggingSettings


class LoggerFactory:
    """로거 생성 및 설정 팩토리"""

    _instance: Optional['LoggerFactory'] = None
    _loggers: Dict[str, logging.Logger] = {}
    _configured: bool = False

    def __new__(cls, settings: LoggingSettings) -> 'LoggerFactory':
        """싱글톤 패턴"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, settings: LoggingSettings):
        if not self._configured:
            self.settings = settings
            self._setup_root_logger()
            self._setup_third_party_loggers()
            self._configured = True

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """로거 인스턴스 반환"""
        if name is None:
            import inspect
            frame = inspect.currentframe().f_back
            name = frame.f_globals.get('__name__', 'app')

        if name in self._loggers:
            return self._loggers[name]

        logger = logging.getLogger(name)
        self._loggers[name] = logger
        return logger

    def _setup_root_logger(self) -> None:
        """루트 로거 설정"""
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.settings.effective_level))

        # 기존 핸들러 모두 제거
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        formatter = logging.Formatter(
            self.settings.format,
            datefmt=self.settings.date_format
        )

        # 콘솔 핸들러
        if self.settings.console_enabled:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

        # 파일 핸들러
        if self.settings.file_enabled:
            self._setup_file_handler(root_logger, formatter)

    def _setup_file_handler(self, logger: logging.Logger, formatter: logging.Formatter) -> None:
        """파일 핸들러 설정"""
        log_path = Path(self.settings.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            self.settings.log_file,
            maxBytes=self.settings.max_file_size,
            backupCount=self.settings.backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def _setup_third_party_loggers(self) -> None:
        """서드파티 로거들 설정"""
        # 레벨 설정
        for logger_name, level in self.settings.third_party_levels.items():
            logger = logging.getLogger(logger_name)
            logger.setLevel(getattr(logging, level.upper()))

        # Silent 로거들
        for logger_name in self.settings.silent_loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.CRITICAL)
            logger.propagate = False


# ================================
# 🎯 전역 팩토리 관리
# ================================

_logger_factory: Optional[LoggerFactory] = None


def get_logger_factory(settings: LoggingSettings) -> LoggerFactory:
    """로거 팩토리 인스턴스 반환"""
    global _logger_factory
    if _logger_factory is None:
        _logger_factory = LoggerFactory(settings)
    return _logger_factory


def _get_default_settings() -> LoggingSettings:
    """기본 로깅 설정 반환 (순환 import 방지)"""
    try:
        from ..app_settings import get_settings
        return get_settings().logging
    except ImportError:
        # 순환 import 방지용 기본 설정
        return LoggingSettings(
            debug_mode=True,
            level="INFO"
        )


# ================================
# 🎯 모듈 레벨 편의 함수들
# ================================

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """로거 인스턴스 반환 (모듈 레벨 함수)"""
    if name is None:
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'app')

    settings = _get_default_settings()
    factory = get_logger_factory(settings)
    return factory.get_logger(name)


def configure_logging(**kwargs) -> None:
    """로깅 시스템 초기화 (모듈 레벨 함수)"""
    settings = _get_default_settings()

    # kwargs로 설정 오버라이드
    if kwargs:
        # 동적으로 설정 업데이트
        settings_dict = settings.dict()
        settings_dict.update(kwargs)
        settings = LoggingSettings(**settings_dict)

    # 팩토리 초기화 (이미 설정된 경우 재설정)
    global _logger_factory
    _logger_factory = LoggerFactory(settings)


def reset_logging() -> None:
    """로깅 시스템 리셋 (테스트용)"""
    global _logger_factory
    _logger_factory = None
