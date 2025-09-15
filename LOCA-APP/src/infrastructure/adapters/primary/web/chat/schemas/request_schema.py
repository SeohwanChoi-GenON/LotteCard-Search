"""
Chat 요청 스키마

채팅 관련 요청 데이터 모델을 정의합니다.
"""

from pydantic import Field, BaseModel

from infrastructure.adapters.primary.web.common.schemas.base_request_schema import BaseRequestData
from infrastructure.adapters.primary.web.common.schemas.gateway_request_scehma import GatewayComm


class ChatRequestData(BaseRequestData):
    """채팅 요청 데이터"""
    user_input: str = Field(
        ...,
        max_length=1000,
        description="사용자 질문 내용",
        example="할인되는 카드 있나요?"
    )


class ChatRequest(BaseModel):
    """채팅 요청"""
    COMM: GatewayComm
    data: ChatRequestData

