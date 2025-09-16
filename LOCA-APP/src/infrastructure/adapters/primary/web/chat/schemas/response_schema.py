"""
Chat 응답 스키마

채팅 관련 응답 데이터 모델을 정의합니다.
"""

from pydantic import BaseModel, Field
from infrastructure.adapters.primary.web.common.schemas.base_schemas import (
    BaseResponse,
    BaseResponseMeta
)


class CompletionResponseMeta(BaseResponseMeta):
    """채팅 응답 메타 스키마"""

    message_id: int = Field(
        ...,
        description="메시지 인덱스",
        example=1
    )


class CompletionResponseData(BaseModel):
    """채팅 응답 데이터 스키마"""

    general_answer: str = Field(
        ...,
        max_length=5000,
        description="AI 생성 답변",
        example="롯데카드를 이용하시면 다양한 할인 혜택을 받으실 수 있습니다..."
    )


class CompletionResponse(BaseResponse):
    """채팅 응답 스키마"""

    meta: CompletionResponseMeta
    data: CompletionResponseData

    class Config:
        json_schema_extra = {
            "example": {
                "meta": {
                    "thread_id": "thread_12345",
                    "message_id": 1,
                    "result_status": "200",
                    "result_status_message": "성공",
                    "timestamp": "2024-01-01T12:00:00Z"
                },
                "data": {
                    "general_answer": "롯데카드를 이용하시면 다양한 할인 혜택을 받으실 수 있습니다...",
                    # "general_answer_template": None
                }
            }
        }