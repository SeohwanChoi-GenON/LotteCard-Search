"""
통신 헤더 스키마

UNO API Gateway 공통 통신 헤더(COMM)를 정의합니다.
"""
import re
from pydantic import BaseModel, Field
from pydantic.v1 import validator


class CommBase(BaseModel):
    """UNO API Gateway 공통 통신 헤더 (COMM)"""
    guid: str = Field(
        ...,
        min_length=31,
        max_length=31,
        description="Global Unique ID (31자리)"
    )

    src_sys_cd: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="요청 출발지 시스템 코드 (3자리)"
    )

    stc_biz_cd: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="요청 출발지 업무 코드 (2자리)"
    )

    gram_prg_no: str = Field(
        default="0",
        description="전문 진행번호"
    )

    gram_no: str = Field(
        default="N",
        description="전문 번호"
    )

    tsmt: str = Field(
        ...,
        min_length=17,
        max_length=17,
        description="요청 타임스탬프 (yyyyMMddhhmmssSSS)"
    )

    @validator('guid', allow_reuse=True)
    def validate_guid_format(cls, v):
        if len(v) != 31:
            raise ValueError('GUID must be exactly 31 characters')
        return v

    @validator('src_sys_cd', allow_reuse=True)
    def validate_src_sys_cd(cls, v):
        if not v.isalpha():
            raise ValueError('Source system code must contain only letters')
        return v.upper()

    @validator('stc_biz_cd', allow_reuse=True)
    def validate_stc_biz_cd(cls, v):
        if not v.isalnum():
            raise ValueError('Business code must be alphanumeric')
        return v.upper()

    @validator('tsmt', allow_reuse=True)
    def validate_timestamp_format(cls, v):
        if not re.match(r'^\d{17}$', v):
            raise ValueError('Timestamp must be 17 digits')
        return v