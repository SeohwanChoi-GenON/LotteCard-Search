"""
웹 어댑터 공통 베이스 스키마

모든 요청/응답의 공통 베이스 클래스를 정의합니다.
"""
from datetime import datetime
from pydantic import BaseModel, Field
from .service_types import ServiceId


class BaseRequest(BaseModel):
    """모든 요청의 공통 베이스 스키마"""
    thread_id: str = Field(
        ...,
        max_length=50,
        description="대화 세션 고유 ID",
        example="thread_12345"
    )
    user_id: str = Field(
        ...,
        max_length=20,
        description="사용자 ID",
        example="user_001"
    )
    service_id: ServiceId = Field(
        ...,
        description="서비스 식별자",
        example=ServiceId.CARD
    )


class BaseResponseMeta(BaseModel):
    """모든 응답 메타의 공통 베이스 스키마"""
    thread_id: str = Field(
        ...,
        description="대화 세션 고유 ID",
        example="thread_12345"
    )
    result_status: str = Field(
        ...,
        description="처리 상태",
        example="200"
    )
    result_status_message: str = Field(
        ...,
        description="처리 상태 메시지",
        example="성공"
    )
    timestamp: datetime = Field(
        ...,
        description="타임스탬프",
        example="2024-01-01T12:00:00Z"
    )


class BaseResponse(BaseModel):
    """모든 응답의 공통 베이스 스키마"""
    meta: BaseResponseMeta