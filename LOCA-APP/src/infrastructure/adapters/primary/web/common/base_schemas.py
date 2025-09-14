"""
웹 어댑터 공통 베이스 스키마

모든 요청/응답의 공통 베이스 클래스를 정의합니다.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ServiceId(str, Enum):
    """서비스 식별자"""
    UNIFIED = "Unified"
    CARD = "Card"
    EVENT = "Event"
    CONTENTS = "Contents"
    COMMERCE = "Commerce"
    MENU = "Menu"


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


class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    error_code: str = Field(
        ...,
        description="에러 코드",
        example="VALIDATION_ERROR"
    )
    error_message: str = Field(
        ...,
        description="에러 메시지",
        example="잘못된 요청입니다."
    )
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="에러 상세 정보",
        example={"thread_id": "thread_12345"}
    )


class RetrievedContent(BaseModel):
    """검색된 컨텐츠 공통 스키마"""
    document_id: str = Field(
        ...,
        description="문서 ID",
        example="doc_001"
    )
    title: str = Field(
        ...,
        description="문서 제목",
        example="롯데카드 혜택 안내"
    )
    content: str = Field(
        ...,
        description="문서 내용",
        example="롯데카드를 이용하면 다양한 혜택을..."
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="관련도 점수",
        example=0.95
    )
    source: str = Field(
        ...,
        description="문서 출처",
        example="card_database"
    )