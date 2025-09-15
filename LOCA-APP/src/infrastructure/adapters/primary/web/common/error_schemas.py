"""
에러 응답 스키마

에러 관련 응답 모델을 정의합니다.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


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