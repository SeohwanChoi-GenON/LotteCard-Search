"""
Suggestion 응답 스키마

연관질문 생성 관련 응답 데이터 모델을 정의합니다.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from infrastructure.adapters.primary.web.common.schemas.base_schemas import BaseResponse, BaseResponseMeta


class SuggestionResponseMeta(BaseResponseMeta):
    """연관질문 응답 메타 스키마"""

    message_id: int = Field(
        ...,
        description="메시지 인덱스",
        example=1
    )


class SuggestionResponseData(BaseModel):
    """연관질문 응답 데이터 스키마"""

    suggestions: Optional[List[str]] = Field(
        None,
        description="추천 연관 질문 목록",
        example=[
            "다른 카드 혜택도 있나요?",
            "카드 신청 방법을 알려주세요",
            "연회비는 얼마인가요?",
            "카드 사용 조건이 궁금합니다"
        ]
    )


class SuggestionResponse(BaseResponse):
    """연관질문 응답 스키마"""

    meta: SuggestionResponseMeta
    data: SuggestionResponseData

    class Config:
        json_schema_extra = {
            "example": {
                "meta": {
                    "thread_id": "thread_12345",
                    "message_id": 1,
                    "result_status": "200",
                    "result_status_message": "연관질문 생성 성공",
                    "timestamp": "2024-01-01T12:00:00Z"
                },
                "data": {
                    "suggestions": [
                        "다른 카드 혜택도 있나요?",
                        "카드 신청 방법을 알려주세요",
                        "연회비는 얼마인가요?",
                        "카드 사용 조건이 궁금합니다"
                    ]
                }
            }
        }
