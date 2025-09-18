from typing import Dict, List

from pydantic import BaseModel, Field


class LoggingSettings(BaseModel):
    """로깅 시스템 설정"""

    # === 기본 설정 ===
    level: str = Field("INFO", description="로그 레벨")
    debug_mode: bool = Field(False, description="디버그 모드")

    # === 출력 설정 ===
    console_enabled: bool = Field(True, description="콘솔 출력 활성화")
    file_enabled: bool = Field(True, description="파일 출력 활성화")

    # === 파일 설정 ===
    log_file: str = Field("logs/app.log", description="로그 파일 경로")
    max_file_size: int = Field(10 * 1024 * 1024, description="최대 파일 크기 (bytes)")
    backup_count: int = Field(5, description="백업 파일 수")

    # === 포맷 설정 ===
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - "
                "[%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s",
        description="로그 포맷"
    )

    date_format: str = Field("%Y-%m-%d %H:%M:%S", description="날짜 포맷")

    # === 서드파티 로거 설정 ===
    third_party_levels: Dict[str, str] = Field(
        default_factory=lambda: {
            "uvicorn": "INFO",
            "uvicorn.access": "WARNING",
            "fastapi": "INFO",
            "httpx": "WARNING",
            "urllib3.connectionpool": "WARNING",
        },
        description="서드파티 로거 레벨"
    )

    # === 제외할 로거 ===
    silent_loggers: List[str] = Field(
        default_factory=lambda: ["asyncio", "concurrent.futures"],
        description="완전히 제외할 로거들"
    )

    @property
    def effective_level(self) -> str:
        """실제 적용할 로그 레벨 (debug_mode 고려)"""
        if self.debug_mode:
            return "DEBUG"
        return self.level.upper()

    @property
    def uvicorn_log_level(self) -> str:
        """Uvicorn용 로그 레벨 (소문자)"""
        return self.effective_level.lower()