"""
Suggestion 요청 스키마

연관질문 생성 관련 요청 데이터 모델을 정의합니다.
"""

from typing import Optional
from pydantic import Field, validator, BaseModel

from ...common.schemas.base_request_schema import BaseRequestData
from ...common.schemas.gateway_request_scehma import GatewayComm
from ...common.validators import validate_user_input, validate_message_id


class SuggestionRequestData(BaseRequestData):
    """연관질문 생성 요청 스키마"""

    message_id: int = Field(
        ...,
        ge=1,
        description="메시지 인덱스",
        example=1
    )

    @validator('message_id')
    def validate_message_id_field(cls, v):
        """메시지 ID 검증"""
        return validate_message_id(v)

class SuggestionRequest(SuggestionRequestData):
    """채팅 요청"""
    pass
