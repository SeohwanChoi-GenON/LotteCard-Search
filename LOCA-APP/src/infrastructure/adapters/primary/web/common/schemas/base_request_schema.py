from pydantic import BaseModel, Field

from infrastructure.adapters.primary.web.common.schemas.base_schemas import ServiceId


class BaseRequestData(BaseModel):
    """모든 요청의 공통 베이스 스키마"""
    thread_id: str = Field(
        ...,
        max_length=50,
        description="대화 세션 고유 ID",
        example="thread_12345"
    )
    service_id: ServiceId = Field(
        ...,
        description="서비스 식별자",
        example=ServiceId.CARD
    )
