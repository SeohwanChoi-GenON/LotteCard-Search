"""
Chat 요청 스키마

채팅 관련 요청 데이터 모델을 정의합니다.
"""

from pydantic import Field

from infrastructure.adapters.primary.web.common.schemas.base_request_schema import BaseRequestData


class CompletionRequestData(BaseRequestData):
    """채팅 요청 데이터"""
    user_id: str = Field(
        ...,
        max_length=20,
        description="사용자 ID",
        example="user_001"
    )

    user_input: str = Field(
        ...,
        max_length=1000,
        description="사용자 질문 내용",
        example="할인되는 카드 있나요?"
    )

    search_type: str = Field(
        ...,
        max_length=50,
        description="검색 유형",
        example="internal"
    )


class CompletionRequest(CompletionRequestData):
    """채팅 요청"""
    pass
