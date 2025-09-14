from pydantic import Field

from infrastructure.adapters.primary.web.schemas.common.base_schema import BaseMetaResponse


class ChatMetaResponse(BaseMetaResponse):
    thread_id: str = Field(..., max_length=50, description="대화 세션 고유 ID")
    message_id: int = Field(..., description="메시지 인덱스")
