"""Gateway 설정"""

from pydantic import Field
from pydantic_settings import BaseSettings


class GatewaySettings(BaseSettings):
    """Gateway 설정"""

    # === 기본 활성화 설정 ===
    enabled: bool = Field(
        default=True,
        description="Gateway 통합 기능 활성화 여부",
        env="GATEWAY_ENABLED"
    )

    # === 통신 방식 설정 ===
    header_mode: bool = Field(
        default=True,
        description="HTTP 헤더에서 Gateway 정보 추출",
        env="GATEWAY_HEADER_MODE"
    )

    body_mode: bool = Field(
        default=False,
        description="요청 바디(COMM 필드)에서 Gateway 정보 추출",
        env="GATEWAY_BODY_MODE"
    )

    # === 필수 필드 검증 ===
    require_guid: bool = Field(
        default=True,
        description="GUID 필드 필수 여부",
        env="GATEWAY_REQUIRE_GUID"
    )

    require_tsmt: bool = Field(
        default=True,
        description="TSMT(타임스탬프) 필드 필수 여부",
        env="GATEWAY_REQUIRE_TSMT"
    )

    strict_validation: bool = Field(
        default=False,
        description="엄격한 Gateway 헤더 검증 (누락 시 오류)",
        env="GATEWAY_STRICT_VALIDATION"
    )

    # === 기본값 설정 ===
    default_src_sys_cd: str = Field(
        default="GAI",
        description="기본 출발지 시스템 코드",
        env="GATEWAY_DEFAULT_SRC_SYS_CD"
    )

    default_stc_biz_cdd: str = Field(
        default="BR",
        description="기본 출발지 업무 코드",
        env="GATEWAY_DEFAULT_STC_BIZ_CDD"
    )

    default_gram_prg_no: str = Field(
        default="00",
        description="기본 전문 진행번호",
        env="GATEWAY_DEFAULT_GRAM_PRG_NO"
    )

    default_gran_no: str = Field(
        default="N",
        description="기본 전문 번호",
        env="GATEWAY_DEFAULT_GRAN_NO"
    )

    # === 타임아웃 및 성능 설정 ===
    extraction_timeout: float = Field(
        default=5.0,
        description="Gateway 정보 추출 타임아웃(초)",
        env="GATEWAY_EXTRACTION_TIMEOUT"
    )

    max_body_size: int = Field(
        default=1024 * 1024,
        description="바디 파싱 최대 크기(bytes)",
        env="GATEWAY_MAX_BODY_SIZE"
    )

    # === 로깅 설정 ===
    log_gateway_info: bool = Field(
        default=False,
        description="Gateway 정보 로깅 여부",
        env="GATEWAY_LOG_INFO"
    )

    log_missing_headers: bool = Field(
        default=True,
        description="누락된 헤더 로깅 여부",
        env="GATEWAY_LOG_MISSING_HEADERS"
    )

    class Config:
        env_file = ".env"
        extra = "ignore"

