"""
Chat 요청 스키마

채팅 관련 요청 데이터 모델을 정의합니다.
"""

from pydantic import Field
from infrastructure.adapters.primary.web.common.base_schemas import BaseRequest


class ChatRequest(BaseRequest):
    """채팅 요청 스키마"""

    user_input: str = Field(
        ...,
        max_length=1000,
        description="사용자 질문 내용",
        example="할인되는 카드 있나요?"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "thread_id": "thread_12345",
                "user_id": "user_001",
                "service_id": "Card",
                "user_input": "할인되는 카드 있나요?"
            }
        }