from pydantic import BaseModel, Field

from infrastructure.adapters.primary.web.schemas.chat.context.context_schema import ChatContextResponse
from infrastructure.adapters.primary.web.schemas.chat.data.data_schema import ChatDataResponse
from infrastructure.adapters.primary.web.schemas.chat.meta.meta_schema import ChatMetaResponse
from infrastructure.adapters.primary.web.schemas.common.base_schema import ServiceType


class ChatRequest(BaseModel):
    thread_id: str = Field(..., max_length=50, description="대화 세션 고유 ID")
    user_id: str = Field(..., max_length=20, description="사용자 ID")
    service_id: ServiceType = Field(..., description="서비스 식별자")
    user_input: str = Field(..., max_length=1000, description="사용자 질문 내용")

class ChatResponse(BaseModel):
    meta: ChatMetaResponse
    data: ChatDataResponse
    context: ChatContextResponse
