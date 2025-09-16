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

    user_input: str = Field(
        ...,
        max_length=1000,
        description="사용자 질문 내용",
        example="할인되는 카드 있나요?"
    )

    generated_answer: Optional[str] = Field(
        None,
        max_length=5000,
        description="LLM 답변 내용",
        example="롯데카드를 이용하시면 다양한 할인 혜택을 받으실 수 있습니다..."
    )

    @validator('message_id')
    def validate_message_id_field(cls, v):
        """메시지 ID 검증"""
        return validate_message_id(v)

    @validator('user_input')
    def validate_user_input_field(cls, v):
        """사용자 입력 검증"""
        return validate_user_input(v, max_length=1000)

    @validator('generated_answer')
    def validate_generated_answer_field(cls, v):
        """생성된 답변 검증"""
        if v is not None and len(v.strip()) == 0:
            raise ValueError("generated_answer는 공백만으로 구성될 수 없습니다.")
        return v

class SuggestionRequest(BaseModel):
    """채팅 요청"""
    COMM: GatewayComm
    data: SuggestionRequestData
